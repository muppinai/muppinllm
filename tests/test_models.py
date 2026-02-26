"""
Tests for MuppinLLM models.
"""
import pytest
from datetime import datetime, timezone
from muppinllm.models import (
    TokenData,
    TechnicalAnalysis,
    FundamentalAnalysis,
    SentimentAnalysis,
    AnalysisResult,
    Verdict
)


class TestVerdict:
    """Tests for Verdict enum."""
    
    def test_verdict_values(self):
        """Test all verdict values exist."""
        assert Verdict.EXTREMELY_BULLISH.value == "EXTREMELY_BULLISH"
        assert Verdict.BULLISH.value == "BULLISH"
        assert Verdict.NEUTRAL.value == "NEUTRAL"
        assert Verdict.BEARISH.value == "BEARISH"
        assert Verdict.EXTREMELY_BEARISH.value == "EXTREMELY_BEARISH"
    
    def test_verdict_from_string(self):
        """Test creating verdict from string."""
        verdict = Verdict("BULLISH")
        assert verdict == Verdict.BULLISH


class TestTokenData:
    """Tests for TokenData dataclass."""
    
    def test_create_token_data(self):
        """Test creating token data."""
        token = TokenData(
            contract_address="test123",
            name="Test Token",
            symbol="TEST",
            price_usd=1.50,
            price_change_24h=5.5
        )
        
        assert token.contract_address == "test123"
        assert token.name == "Test Token"
        assert token.symbol == "TEST"
        assert token.price_usd == 1.50
        assert token.price_change_24h == 5.5
    
    def test_token_data_defaults(self):
        """Test default values."""
        token = TokenData(contract_address="test")
        
        assert token.name is None
        assert token.price_usd is None
        assert token.price_history == []


class TestAnalysisResult:
    """Tests for AnalysisResult dataclass."""
    
    @pytest.fixture
    def sample_result(self):
        """Create a sample analysis result."""
        token = TokenData(
            contract_address="test123",
            name="Test Token",
            symbol="TEST",
            price_usd=1.50,
            price_change_24h=5.5,
            volume_24h=100000,
            liquidity_usd=500000,
            fdv=10000000,
            market_cap=5000000
        )
        
        technical = TechnicalAnalysis(
            rsi_14=55.0,
            rsi_signal="neutral",
            macd_trend="bullish",
            trend_direction="uptrend",
            score=65.0,
            signal="BULLISH",
            summary="Strong uptrend with bullish momentum"
        )
        
        fundamental = FundamentalAnalysis(
            liquidity_usd=500000,
            liquidity_rating="good",
            volume_24h=100000,
            volume_rating="moderate",
            score=60.0,
            signal="NEUTRAL",
            summary="Good liquidity with moderate volume"
        )
        
        sentiment = SentimentAnalysis(
            overall_sentiment="POSITIVE",
            sentiment_score=70.0,
            signal="BULLISH",
            summary="Positive market sentiment"
        )
        
        return AnalysisResult(
            token=token,
            technical=technical,
            fundamental=fundamental,
            sentiment=sentiment,
            verdict=Verdict.BULLISH,
            strength=70,
            combined_score=65.0,
            ai_summary="Token showing strong bullish signals",
            ai_recommendation="Consider entry on pullbacks",
            risk_factors=["High volatility"],
            opportunities=["Growing community"]
        )
    
    def test_to_dict(self, sample_result):
        """Test conversion to dictionary."""
        data = sample_result.to_dict()
        
        assert data["verdict"] == "BULLISH"
        assert data["strength"] == 70
        assert data["combined_score"] == 65.0
        assert data["token"]["symbol"] == "TEST"
        assert data["technical"]["score"] == 65.0
        assert "analyzed_at" in data
    
    def test_str_representation(self, sample_result):
        """Test string representation."""
        output = str(sample_result)
        
        assert "TEST" in output
        assert "BULLISH" in output
        assert "65" in output or "65.0" in output
