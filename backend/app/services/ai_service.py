"""Main AI Service orchestrating all components"""
from typing import Dict, Any, List, Optional
from .gemini_service import GeminiService
from .knowledge_service import KnowledgeService
from .time_service import TimeService
from .translation_service import TranslationService
import asyncio


class AIService:
    """Main AI Service integrating Gemini and other services"""
    
    def __init__(
        self,
        gemini_service: GeminiService,
        knowledge_service: KnowledgeService,
        time_service: TimeService,
        translation_service: TranslationService
    ):
        """Initialize AI Service with all dependencies
        
        Args:
            gemini_service: Gemini AI service instance
            knowledge_service: Knowledge base service instance
            time_service: Time service instance
            translation_service: Translation service instance
        """
        self.gemini_service = gemini_service
        self.knowledge_service = knowledge_service
        self.time_service = time_service
        self.translation_service = translation_service
        self.sessions: Dict[str, List[Dict]] = {}
    
    async def process_message(
        self, 
        message: str, 
        session_id: str,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Process user message and generate response
        
        Args:
            message: User's message
            session_id: Session identifier for conversation tracking
            stream: Whether to stream the response
            
        Returns:
            Response dictionary with message and metadata
        """
        try:
            # Get or create session
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            
            context = self.sessions[session_id]
            
            # Use Gemini for intent detection
            intent_analysis = await self.gemini_service.analyze_intent(message)
            
            intent = intent_analysis.get('intent', 'general')
            confidence = intent_analysis.get('confidence', 0.5)
            
            # Route based on intent
            response_text = ""
            metadata = {
                "intent": intent,
                "confidence": confidence,
                "timestamp": self.time_service.get_current_time()['formatted']
            }
            
            if intent == 'greeting':
                response_text = await self._handle_greeting(message, context)
                
            elif intent == 'time_query':
                response_text = self._handle_time_query()
                
            elif intent == 'knowledge_search':
                response_text = await self._handle_knowledge_search(
                    message, 
                    intent_analysis.get('query', message),
                    context
                )
                
            elif intent == 'translation':
                response_text = await self._handle_translation(message)
                
            elif intent == 'help':
                response_text = self._handle_help()
                
            else:
                # Use Gemini for general conversation
                response_text = await self.gemini_service.generate_response(
                    message, 
                    context,
                    stream=stream
                )
            
            # Update conversation history
            self.sessions[session_id].append({
                "role": "user",
                "content": message,
                "timestamp": metadata['timestamp']
            })
            
            self.sessions[session_id].append({
                "role": "assistant",
                "content": response_text,
                "timestamp": metadata['timestamp']
            })
            
            # Keep only last 20 messages to manage memory
            if len(self.sessions[session_id]) > 20:
                self.sessions[session_id] = self.sessions[session_id][-20:]
            
            return {
                "response": response_text,
                "metadata": metadata,
                "session_id": session_id
            }
            
        except Exception as e:
            print(f"Error processing message: {e}")
            return {
                "response": "Xin lỗi, đã có lỗi xảy ra khi xử lý tin nhắn của bạn. Vui lòng thử lại.",
                "metadata": {
                    "intent": "error",
                    "error": str(e)
                },
                "session_id": session_id
            }
    
    async def _handle_greeting(self, message: str, context: List[Dict]) -> str:
        """Handle greeting messages"""
        greetings = [
            "Xin chào! Tôi là trợ lý AI của công ty. Tôi có thể giúp gì cho bạn?",
            "Chào bạn! Tôi sẵn sàng hỗ trợ bạn. Bạn cần giúp đỡ gì?",
            "Xin chào! Rất vui được hỗ trợ bạn hôm nay. Bạn muốn biết điều gì?"
        ]
        
        # Use first greeting if no context, otherwise use Gemini for more natural response
        if len(context) == 0:
            return greetings[0]
        else:
            return await self.gemini_service.generate_response(message, context)
    
    def _handle_time_query(self) -> str:
        """Handle time-related queries"""
        time_info = self.time_service.get_current_time()
        return f"Hiện tại là {time_info['vietnamese']}"
    
    async def _handle_knowledge_search(
        self, 
        original_message: str,
        query: str, 
        context: List[Dict]
    ) -> str:
        """Handle knowledge base searches"""
        # Check if knowledge base is loaded
        stats = self.knowledge_service.get_stats()
        
        if not stats.get('loaded', False):
            return "Hiện tại chưa có dữ liệu trong cơ sở tri thức. Vui lòng tải lên file CSV để tôi có thể hỗ trợ bạn."
        
        # Get CSV content
        csv_content = self.knowledge_service.get_csv_content()
        
        if csv_content:
            # Use Gemini to extract knowledge
            response = await self.gemini_service.extract_knowledge(
                csv_content,
                query
            )
            return response
        else:
            # Fallback to simple search
            results = self.knowledge_service.search(query)
            
            if results:
                formatted = "Tìm thấy thông tin sau:\n\n"
                for i, result in enumerate(results, 1):
                    formatted += f"{i}. {str(result)}\n"
                return formatted
            else:
                return "Xin lỗi, tôi không tìm thấy thông tin liên quan trong cơ sở tri thức."
    
    async def _handle_translation(self, message: str) -> str:
        """Handle translation requests"""
        # Extract text to translate from message
        # Simple implementation - can be enhanced
        return await self.translation_service.translate(message)
    
    def _handle_help(self) -> str:
        """Handle help requests"""
        return """
🤖 **Trợ lý AI Công ty - Hướng dẫn sử dụng**

Tôi có thể giúp bạn:

✅ **Trò chuyện tự nhiên** - Hỏi bất kỳ câu hỏi nào bằng tiếng Việt
✅ **Tra cứu thông tin** - Tìm kiếm trong cơ sở tri thức công ty
✅ **Kiểm tra thời gian** - Hỏi "mấy giờ rồi?" hoặc "bây giờ là mấy giờ?"
✅ **Dịch thuật** - Dịch từ tiếng Việt sang tiếng Anh và ngược lại
✅ **Tải file CSV** - Upload file dữ liệu để tôi phân tích

**Ví dụ câu hỏi:**
- "Tìm thông tin về nhân viên X"
- "Mấy giờ rồi?"
- "Dịch 'xin chào' sang tiếng Anh"
- "Hướng dẫn sử dụng hệ thống Y"

Hãy thử hỏi tôi bất cứ điều gì! 😊
        """.strip()
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of conversation messages
        """
        return self.sessions.get(session_id, [])
    
    def clear_session(self, session_id: str) -> bool:
        """Clear conversation history for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Success status
        """
        if session_id in self.sessions:
            self.sessions[session_id] = []
            return True
        return False
