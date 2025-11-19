"""Basic tests for AI services"""
import pytest
from app.services.gemini_service import GeminiService
from app.services.knowledge_service import KnowledgeService
from app.services.time_service import TimeService
from app.services.translation_service import TranslationService
from app.services.ai_service import AIService


class TestGeminiService:
    """Tests for Gemini service"""
    
    def test_fallback_intent_detection_greeting(self):
        """Test fallback intent detection for greetings"""
        service = GeminiService("dummy_key")
        result = service._fallback_intent_detection("xin chào")
        
        assert result["intent"] == "greeting"
        assert result["confidence"] > 0.8
    
    def test_fallback_intent_detection_time(self):
        """Test fallback intent detection for time queries"""
        service = GeminiService("dummy_key")
        result = service._fallback_intent_detection("mấy giờ rồi?")
        
        assert result["intent"] == "time_query"
        assert result["confidence"] > 0.8
    
    def test_fallback_intent_detection_help(self):
        """Test fallback intent detection for help requests"""
        service = GeminiService("dummy_key")
        result = service._fallback_intent_detection("giúp tôi")
        
        assert result["intent"] == "help"


class TestKnowledgeService:
    """Tests for Knowledge service"""
    
    @pytest.mark.asyncio
    async def test_load_csv(self):
        """Test CSV loading"""
        service = KnowledgeService()
        
        csv_content = b"name,age\nJohn,30\nJane,25"
        success = await service.load_csv(csv_content, "test.csv")
        
        assert success is True
        assert service.knowledge_data is not None
        assert len(service.knowledge_data) == 2
    
    def test_get_stats_no_data(self):
        """Test stats when no data loaded"""
        service = KnowledgeService()
        stats = service.get_stats()
        
        assert stats["loaded"] is False
    
    @pytest.mark.asyncio
    async def test_get_stats_with_data(self):
        """Test stats with loaded data"""
        service = KnowledgeService()
        csv_content = b"name,age\nJohn,30"
        await service.load_csv(csv_content, "test.csv")
        
        stats = service.get_stats()
        
        assert stats["loaded"] is True
        assert stats["rows"] == 1
        assert stats["columns"] == 2


class TestTimeService:
    """Tests for Time service"""
    
    def test_get_current_time(self):
        """Test getting current time"""
        service = TimeService()
        result = service.get_current_time()
        
        assert "time" in result
        assert "date" in result
        assert "day_of_week" in result
        assert "formatted" in result
        assert "vietnamese" in result


class TestTranslationService:
    """Tests for Translation service"""
    
    @pytest.mark.asyncio
    async def test_translate_vi_to_en(self):
        """Test Vietnamese to English translation"""
        service = TranslationService()
        result = await service.translate("xin chào", "vi", "en")
        
        assert result == "hello"
    
    def test_detect_language_vietnamese(self):
        """Test Vietnamese language detection"""
        service = TranslationService()
        result = service.detect_language("xin chào")
        
        assert result == "vi"
    
    def test_detect_language_english(self):
        """Test English language detection"""
        service = TranslationService()
        result = service.detect_language("hello")
        
        assert result == "en"


class TestAIService:
    """Tests for AI service integration"""
    
    @pytest.fixture
    def ai_service(self):
        """Create AI service instance for testing"""
        gemini_service = GeminiService("dummy_key")
        knowledge_service = KnowledgeService()
        time_service = TimeService()
        translation_service = TranslationService()
        
        return AIService(
            gemini_service=gemini_service,
            knowledge_service=knowledge_service,
            time_service=time_service,
            translation_service=translation_service
        )
    
    def test_handle_time_query(self, ai_service):
        """Test time query handling"""
        result = ai_service._handle_time_query()
        
        assert "Hiện tại là" in result
    
    def test_handle_help(self, ai_service):
        """Test help request handling"""
        result = ai_service._handle_help()
        
        assert "Trợ lý AI Công ty" in result
        assert "Hướng dẫn sử dụng" in result
