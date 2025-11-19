"""Translation Service"""
from typing import Dict


class TranslationService:
    """Simple translation service"""
    
    def __init__(self):
        # Basic Vietnamese-English dictionary
        self.translations = {
            'xin chào': 'hello',
            'cảm ơn': 'thank you',
            'tạm biệt': 'goodbye',
            'vâng': 'yes',
            'không': 'no',
        }
    
    async def translate(self, text: str, source_lang: str = 'vi', target_lang: str = 'en') -> str:
        """Translate text (basic implementation)
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        text_lower = text.lower().strip()
        
        if source_lang == 'vi' and target_lang == 'en':
            return self.translations.get(text_lower, text)
        elif source_lang == 'en' and target_lang == 'vi':
            # Reverse lookup
            reverse = {v: k for k, v in self.translations.items()}
            return reverse.get(text_lower, text)
        
        return text
    
    def detect_language(self, text: str) -> str:
        """Detect language of text
        
        Args:
            text: Input text
            
        Returns:
            Language code ('vi' or 'en')
        """
        # Simple detection based on Vietnamese characters
        vietnamese_chars = "àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ"
        
        if any(c in text.lower() for c in vietnamese_chars):
            return 'vi'
        return 'en'
