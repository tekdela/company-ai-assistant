"""Gemini AI Service for Natural Language Processing"""
import google.generativeai as genai
from typing import Dict, Any, List, Optional, AsyncIterator
import json
import asyncio
from datetime import datetime


class GeminiService:
    """Service for interacting with Google Gemini AI"""
    
    def __init__(self, api_key: str):
        """Initialize Gemini service with API key
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat_sessions = {}
        
    async def generate_response(
        self, 
        prompt: str, 
        context: Optional[List[Dict]] = None,
        stream: bool = False
    ) -> str:
        """Generate AI response using Gemini
        
        Args:
            prompt: User's message or prompt
            context: Conversation history context
            stream: Whether to stream the response
            
        Returns:
            AI-generated response text
        """
        try:
            # Build enhanced prompt with context
            full_prompt = self._build_prompt_with_context(prompt, context)
            
            if stream:
                response = await self._generate_streaming_response(full_prompt)
                return response
            else:
                # Run in executor to avoid blocking
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None, 
                    lambda: self.model.generate_content(full_prompt)
                )
                return response.text
                
        except Exception as e:
            print(f"Gemini generation error: {e}")
            return "Xin lỗi, tôi gặp sự cố khi xử lý yêu cầu của bạn. Vui lòng thử lại."
    
    async def _generate_streaming_response(self, prompt: str) -> str:
        """Generate streaming response (for future implementation)"""
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: self.model.generate_content(prompt)
        )
        return response.text
    
    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """Analyze user intent using Gemini AI
        
        Args:
            message: User's message
            
        Returns:
            Dictionary containing intent analysis results
        """
        try:
            intent_prompt = f"""
            Phân tích ý định của người dùng trong tin nhắn sau (bằng tiếng Việt):
            "{message}"
            
            Trả về kết quả dưới dạng JSON với cấu trúc:
            {{
                "intent": "knowledge_search|greeting|time_query|help|translation|general",
                "confidence": 0.0-1.0,
                "entities": {{"key": "value"}},
                "language": "vi|en",
                "query": "extracted search query if applicable"
            }}
            
            Chỉ trả về JSON, không có text khác.
            """
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(intent_prompt)
            )
            
            # Parse JSON response
            result_text = response.text.strip()
            # Remove markdown code blocks if present
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
            
            result = json.loads(result_text.strip())
            return result
            
        except Exception as e:
            print(f"Intent analysis error: {e}")
            # Fallback to simple rule-based intent detection
            return self._fallback_intent_detection(message)
    
    def _fallback_intent_detection(self, message: str) -> Dict[str, Any]:
        """Simple rule-based intent detection as fallback"""
        message_lower = message.lower()
        
        # Greeting patterns
        greetings = ['xin chào', 'chào', 'hello', 'hi', 'hey']
        if any(greeting in message_lower for greeting in greetings):
            return {
                "intent": "greeting",
                "confidence": 0.9,
                "entities": {},
                "language": "vi" if any(c in message for c in "àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ") else "en",
                "query": None
            }
        
        # Time query patterns
        time_keywords = ['giờ', 'time', 'mấy giờ', 'bây giờ', 'now']
        if any(keyword in message_lower for keyword in time_keywords):
            return {
                "intent": "time_query",
                "confidence": 0.85,
                "entities": {},
                "language": "vi",
                "query": None
            }
        
        # Translation patterns
        translation_keywords = ['dịch', 'translate', 'nghĩa là gì']
        if any(keyword in message_lower for keyword in translation_keywords):
            return {
                "intent": "translation",
                "confidence": 0.8,
                "entities": {},
                "language": "vi",
                "query": message
            }
        
        # Help patterns
        help_keywords = ['help', 'giúp', 'hỗ trợ', 'hướng dẫn']
        if any(keyword in message_lower for keyword in help_keywords):
            return {
                "intent": "help",
                "confidence": 0.85,
                "entities": {},
                "language": "vi",
                "query": None
            }
        
        # Default to knowledge search
        return {
            "intent": "knowledge_search",
            "confidence": 0.6,
            "entities": {},
            "language": "vi" if any(c in message for c in "àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ") else "en",
            "query": message
        }
    
    async def extract_knowledge(
        self, 
        csv_content: str, 
        query: str,
        max_rows: int = 100
    ) -> str:
        """Extract relevant knowledge from CSV data using Gemini
        
        Args:
            csv_content: CSV data as string
            query: User's search query
            max_rows: Maximum rows to process
            
        Returns:
            Extracted and formatted knowledge response
        """
        try:
            # Truncate CSV if too long to avoid token limits
            lines = csv_content.split('\n')
            if len(lines) > max_rows:
                csv_content = '\n'.join(lines[:max_rows])
            
            knowledge_prompt = f"""
            Dựa trên dữ liệu CSV sau:
            {csv_content}
            
            Hãy trả lời câu hỏi: "{query}"
            
            Yêu cầu:
            - Trả lời bằng tiếng Việt
            - Ngắn gọn, súc tích
            - Chỉ sử dụng thông tin từ dữ liệu được cung cấp
            - Nếu không tìm thấy thông tin, hãy nói rõ
            """
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(knowledge_prompt)
            )
            
            return response.text
            
        except Exception as e:
            print(f"Knowledge extraction error: {e}")
            return "Xin lỗi, tôi không thể tìm thấy thông tin phù hợp trong cơ sở tri thức."
    
    def _build_prompt_with_context(
        self, 
        prompt: str, 
        context: Optional[List[Dict]] = None
    ) -> str:
        """Build enhanced prompt with conversation context
        
        Args:
            prompt: Current user message
            context: Previous conversation messages
            
        Returns:
            Enhanced prompt with context
        """
        if not context:
            return f"""
            Bạn là trợ lý AI thông minh cho công ty, hỗ trợ nhân viên bằng tiếng Việt.
            
            Người dùng hỏi: {prompt}
            
            Hãy trả lời một cách thân thiện, chuyên nghiệp và hữu ích.
            """
        
        # Build conversation history
        history = []
        for msg in context[-5:]:  # Last 5 messages for context
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            history.append(f"{role.capitalize()}: {content}")
        
        return f"""
        Bạn là trợ lý AI thông minh cho công ty, hỗ trợ nhân viên bằng tiếng Việt.
        
        Lịch sử hội thoại:
        {chr(10).join(history)}
        
        Người dùng hỏi: {prompt}
        
        Hãy trả lời một cách thân thiện, chuyên nghiệp và hữu ích, dựa trên ngữ cảnh cuộc hội thoại.
        """
    
    async def generate_streaming(self, prompt: str, context: Optional[List[Dict]] = None) -> AsyncIterator[str]:
        """Generate streaming response (placeholder for future implementation)"""
        # For now, return the full response as a single chunk
        response = await self.generate_response(prompt, context, stream=False)
        yield response
