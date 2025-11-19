"""
Translation Service - Vietnamese ↔ Japanese dictionary-based translation
"""
from typing import Dict, Optional

# Vietnamese to Japanese dictionary with technical and business terms
VI_JA_DICTIONARY = {
    # Common greetings
    "xin chào": "こんにちは (konnichiwa)",
    "chào": "こんにちは (konnichiwa)",
    "cảm ơn": "ありがとう (arigatou)",
    "tạm biệt": "さようなら (sayounara)",
    "xin lỗi": "すみません (sumimasen)",
    "vâng": "はい (hai)",
    "không": "いいえ (iie)",
    
    # Business terms
    "công ty": "会社 (kaisha)",
    "dự án": "プロジェクト (purojekuto)",
    "họp": "会議 (kaigi)",
    "báo cáo": "報告 (houkoku)",
    "công việc": "仕事 (shigoto)",
    "nhân viên": "社員 (shain)",
    "quản lý": "管理 (kanri)",
    "khách hàng": "顧客 (kokyaku)",
    "hợp đồng": "契約 (keiyaku)",
    "thời hạn": "期限 (kigen)",
    
    # Technical terms
    "phần mềm": "ソフトウェア (sofutowea)",
    "lập trình": "プログラミング (puroguramingu)",
    "máy tính": "コンピューター (konpyuutaa)",
    "dữ liệu": "データ (deeta)",
    "hệ thống": "システム (shisutemu)",
    "mạng": "ネットワーク (nettowaaku)",
    "ứng dụng": "アプリケーション (apurikeeshon)",
    "website": "ウェブサイト (webusaito)",
    
    # Time expressions
    "hôm nay": "今日 (kyou)",
    "ngày mai": "明日 (ashita)",
    "hôm qua": "昨日 (kinou)",
    "bây giờ": "今 (ima)",
    "buổi sáng": "朝 (asa)",
    "buổi chiều": "午後 (gogo)",
    "buổi tối": "夜 (yoru)",
    
    # Numbers
    "một": "一 (ichi)",
    "hai": "二 (ni)",
    "ba": "三 (san)",
    "bốn": "四 (shi)",
    "năm": "五 (go)",
    
    # Common phrases
    "tôi không biết": "わかりません (wakarimasen)",
    "làm ơn": "お願いします (onegaishimasu)",
    "tốt": "良い (yoi)",
    "xấu": "悪い (warui)",
    "lớn": "大きい (ookii)",
    "nhỏ": "小さい (chiisai)",
}

# Japanese to Vietnamese (reverse dictionary)
JA_VI_DICTIONARY = {v.split('(')[0].strip(): k for k, v in VI_JA_DICTIONARY.items()}


class TranslationService:
    def __init__(self):
        self.vi_ja_dict = VI_JA_DICTIONARY
        self.ja_vi_dict = JA_VI_DICTIONARY
    
    def translate_vi_to_ja(self, text: str) -> Optional[str]:
        """Translate Vietnamese to Japanese"""
        text_lower = text.lower().strip()
        return self.vi_ja_dict.get(text_lower)
    
    def translate_ja_to_vi(self, text: str) -> Optional[str]:
        """Translate Japanese to Vietnamese"""
        text_clean = text.strip()
        for ja_key, vi_value in self.ja_vi_dict.items():
            if ja_key in text_clean:
                return vi_value
        return None
    
    def translate(self, text: str, target_lang: str = "ja") -> Dict:
        """
        Translate text between Vietnamese and Japanese
        Args:
            text: Text to translate
            target_lang: Target language ('ja' for Japanese, 'vi' for Vietnamese)
        """
        text_clean = text.strip()
        
        if target_lang == "ja":
            # Vietnamese to Japanese
            translation = self.translate_vi_to_ja(text_clean)
            if translation:
                return {
                    "success": True,
                    "original": text_clean,
                    "translation": translation,
                    "source_lang": "vi",
                    "target_lang": "ja"
                }
        else:
            # Japanese to Vietnamese
            translation = self.translate_ja_to_vi(text_clean)
            if translation:
                return {
                    "success": True,
                    "original": text_clean,
                    "translation": translation,
                    "source_lang": "ja",
                    "target_lang": "vi"
                }
        
        # Try auto-detect and translate both ways
        ja_result = self.translate_vi_to_ja(text_clean)
        if ja_result:
            return {
                "success": True,
                "original": text_clean,
                "translation": ja_result,
                "source_lang": "vi",
                "target_lang": "ja"
            }
        
        vi_result = self.translate_ja_to_vi(text_clean)
        if vi_result:
            return {
                "success": True,
                "original": text_clean,
                "translation": vi_result,
                "source_lang": "ja",
                "target_lang": "vi"
            }
        
        return {
            "success": False,
            "message": "Không tìm thấy từ trong từ điển"
        }
    
    def format_translation_response(self, trans_result: Dict) -> str:
        """Format translation result into response string"""
        if not trans_result.get("success"):
            return f"❌ {trans_result.get('message', 'Không thể dịch')}"
        
        if trans_result["source_lang"] == "vi":
            return (
                f"🔄 **Bản dịch:**\n"
                f"🇻🇳 **Tiếng Việt:** {trans_result['original']}\n"
                f"🇯🇵 **日本語:** {trans_result['translation']}"
            )
        else:
            return (
                f"🔄 **Bản dịch:**\n"
                f"🇯🇵 **日本語:** {trans_result['original']}\n"
                f"🇻🇳 **Tiếng Việt:** {trans_result['translation']}"
            )


# Global instance
translation_service = TranslationService()
