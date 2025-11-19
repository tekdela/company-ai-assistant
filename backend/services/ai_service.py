"""
AI Service - Intent detection and response handling
"""
import re
from typing import Dict, List
from .knowledge_service import knowledge_service
from .time_service import time_service
from .translation_service import translation_service


class AIService:
    def __init__(self):
        self.time_keywords = ["mấy giờ", "bây giờ", "thời gian", "nhật bản", "hàn quốc", "mỹ", "giờ", "time"]
        self.translation_keywords = ["dịch", "translate", "tiếng nhật", "tiếng việt", "번역", "翻訳"]
    
    def detect_intent(self, message: str) -> str:
        """
        Detect user intent from message
        Returns: 'time', 'translation', or 'knowledge_search'
        """
        message_lower = message.lower().strip()
        
        # Check for time intent
        if any(keyword in message_lower for keyword in self.time_keywords):
            return "time"
        
        # Check for translation intent
        if any(keyword in message_lower for keyword in self.translation_keywords):
            return "translation"
        
        # Default to knowledge search
        return "knowledge_search"
    
    def extract_timezone(self, message: str) -> str:
        """Extract timezone from message"""
        message_lower = message.lower()
        
        if "nhật" in message_lower or "japan" in message_lower:
            return "japan"
        elif "hàn" in message_lower or "korea" in message_lower:
            return "korea"
        elif "mỹ" in message_lower or "america" in message_lower or "usa" in message_lower:
            return "usa"
        else:
            return "vietnam"
    
    def extract_translation_text(self, message: str) -> str:
        """Extract text to translate from message"""
        # Pattern: "dịch sang tiếng [lang] '[text]'" or "dịch '[text]'"
        patterns = [
            r"dịch sang tiếng (?:nhật|việt|japan|vietnamese)\s+['\"](.+?)['\"]",
            r"dịch\s+['\"](.+?)['\"]",
            r"translate\s+['\"](.+?)['\"]",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(1)
        
        # If no quotes, try to extract after keyword
        if "dịch" in message.lower():
            parts = message.lower().split("dịch", 1)
            if len(parts) > 1:
                text = parts[1].strip()
                # Remove "sang tiếng nhật/việt" prefix
                text = re.sub(r"^sang tiếng (?:nhật|việt|japan|vietnamese)\s+", "", text)
                return text.strip("'\"")
        
        return message
    
    def handle_time_query(self, message: str) -> str:
        """Handle time-related queries"""
        timezone = self.extract_timezone(message)
        time_info = time_service.get_time(timezone)
        return time_service.format_time_response(time_info)
    
    def handle_translation(self, message: str) -> str:
        """Handle translation requests"""
        text_to_translate = self.extract_translation_text(message)
        
        # Determine target language
        target_lang = "ja"  # Default to Japanese
        if "tiếng việt" in message.lower() or "vietnamese" in message.lower():
            target_lang = "vi"
        
        trans_result = translation_service.translate(text_to_translate, target_lang)
        return translation_service.format_translation_response(trans_result)
    
    def handle_knowledge_search(self, message: str) -> str:
        """Handle knowledge base search"""
        results = knowledge_service.search(message)
        
        if not results:
            return (
                "❌ **Không tìm thấy thông tin**\n\n"
                "Hiện tại tôi không thấy thông tin này trong dữ liệu nội bộ được cung cấp. "
                "Bạn vui lòng:\n"
                "**1.** Kiểm tra lại tài liệu gốc\n"
                "**2.** Hỏi người phụ trách/leader để xác nhận thêm"
            )
        
        # Format results
        response = "📋 **Thông tin tìm thấy:**\n\n"
        for idx, result in enumerate(results, 1):
            response += f"**{idx}.** {result['content']}\n\n"
        
        # Add source info
        sources = list(set([r['source'] for r in results]))
        response += f"📄 *Nguồn: {', '.join(sources)}*"
        
        return response
    
    def process_message(self, message: str) -> Dict:
        """
        Process user message and return appropriate response
        """
        if not message or not message.strip():
            return {
                "response": "Xin chào! Tôi là trợ lý AI của công ty. Bạn cần hỗ trợ gì?",
                "intent": "greeting"
            }
        
        # Detect intent
        intent = self.detect_intent(message)
        
        # Handle based on intent
        if intent == "time":
            response = self.handle_time_query(message)
        elif intent == "translation":
            response = self.handle_translation(message)
        else:
            response = self.handle_knowledge_search(message)
        
        return {
            "response": response,
            "intent": intent
        }


# Global instance
ai_service = AIService()
