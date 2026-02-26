"""
Tests for MuppinLLM analyzers.
"""
import pytest
from muppinllm.analyzers import TechnicalAnalyzer, FundamentalAnalyzer, SentimentAnalyzer


class TestTechnicalAnalyzer:
    """Tests for Technical Analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return TechnicalAnalyzer()
    
    def test_analyze_with_valid_prices(self, analyzer):
        """Test technical analysis with valid price data."""
        prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
                  111, 110, 112, 114, 113, 115, 117, 116, 118, 120]
        
        result = analyzer.analyze(
            prices=prices,
            current_price=120,
            price_changes={"h1": 2.0, "h6": 5.0, "h24": 10.0}
        )
        
        assert result.score >= 0 and result.score <= 100
        assert result.signal in ["BULLISH", "BEARISH", "NEUTRAL"]
        assert result.trend_direction in ["uptrend", "downtrend", "sideways"]
    
    def test_analyze_with_insufficient_data(self, analyzer):
        """Test handling of insufficient price data."""
        prices = [100]
        
        result = analyzer.analyze(prices=prices)
        
        assert "Insufficient" in result.summary
    
    def test_rsi_calculation(self, analyzer):
        """Test RSI calculation."""
        # Uptrending prices should have RSI > 50
        uptrend_prices = [100 + i for i in range(20)]
        result = analyzer.analyze(prices=uptrend_prices)
        
        if result.rsi_14:
            assert result.rsi_14 > 50
    
    def test_macd_calculation(self, analyzer):
        """Test MACD calculation."""
        prices = list(range(100, 130))  # Uptrend
        result = analyzer.analyze(prices=prices)
        
        if result.macd_line:
            assert result.macd_trend in ["bullish", "bearish", "neutral"]


class TestFundamentalAnalyzer:
    """Tests for Fundamental Analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return FundamentalAnalyzer()
    
    def test_analyze_high_liquidity(self, analyzer):
        """Test analysis with high liquidity."""
        token_data = {
            "liquidity_usd": 1_500_000,
            "volume_24h": 500_000,
            "fdv": 10_000_000,
            "market_cap": 5_000_000,
            "pair_created_at": 1609459200000,  # Jan 1, 2021
            "all_pairs": [{"dexId": "raydium"}, {"dexId": "orca"}]
        }
        
        result = analyzer.analyze(token_data)
        
        assert result.liquidity_rating == "excellent"
        assert result.score > 50  # Should be bullish
    
    def test_analyze_low_liquidity(self, analyzer):
        """Test analysis with low liquidity."""
        token_data = {
            "liquidity_usd": 500,
            "volume_24h": 100,
            "all_pairs": []
        }
        
        result = analyzer.analyze(token_data)
        
        assert result.liquidity_rating == "very_low"
        assert result.score < 50  # Should be bearish
    
    def test_maturity_rating(self, analyzer):
        """Test token maturity rating."""
        # Very old token
        import time
        old_timestamp = (time.time() - 400 * 24 * 60 * 60) * 1000  # 400 days ago
        
        token_data = {
            "liquidity_usd": 100_000,
            "volume_24h": 10_000,
            "pair_created_at": old_timestamp,
            "all_pairs": []
        }
        
        result = analyzer.analyze(token_data)
        
        assert result.maturity_rating == "mature"


class TestSentimentAnalyzer:
    """Tests for Sentiment Analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        return SentimentAnalyzer()
    
    def test_analyze_positive_sentiment(self, analyzer):
        """Test with positive price action."""
        token_data = {
            "twitter": "https://twitter.com/test",
            "telegram": "https://t.me/test",
            "txns": {
                "h24": {"buys": 100, "sells": 20}
            }
        }
        
        result = analyzer.analyze(
            token_data,
            price_changes={"h1": 10, "h6": 20, "h24": 30}
        )
        
        assert result.sentiment_score > 50
        assert result.signal in ["BULLISH", "NEUTRAL"]
    
    def test_analyze_negative_sentiment(self, analyzer):
        """Test with negative price action."""
        token_data = {
            "txns": {
                "h24": {"buys": 20, "sells": 100}
            }
        }
        
        result = analyzer.analyze(
            token_data,
            price_changes={"h1": -10, "h6": -20, "h24": -30}
        )
        
        assert result.sentiment_score < 50
    
    def test_community_activity_rating(self, analyzer):
        """Test community activity rating."""
        # Active community
        token_data = {
            "twitter": "https://twitter.com/test",
            "telegram": "https://t.me/test",
            "discord": "https://discord.gg/test",
            "txns": {}
        }
        
        coingecko_data = {
            "community_data": {
                "twitter_followers": 5000,
                "telegram_channel_user_count": 2000
            }
        }
        
        result = analyzer.analyze(token_data, coingecko_data)
        
        assert result.community_activity in ["very_active", "active"]
