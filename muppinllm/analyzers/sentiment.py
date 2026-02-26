"""
Sentiment analysis module for MuppinLLM.
Analyzes social media sentiment and community activity.
"""
from typing import Dict, Any, Optional, List, Tuple
from ..models import SentimentAnalysis


class SentimentAnalyzer:
    """
    Sentiment analyzer for crypto tokens.
    
    Analyzes:
    - Social media mentions and sentiment
    - Community activity levels
    - News sentiment
    - Influencer activity
    
    Note: For production use, integrate with Twitter API, news APIs,
    and sentiment analysis services.
    """
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        pass
    
    def analyze(
        self,
        token_data: Dict[str, Any],
        coingecko_data: Optional[Dict[str, Any]] = None,
        social_data: Optional[Dict[str, Any]] = None,
        price_changes: Optional[Dict[str, float]] = None
    ) -> SentimentAnalysis:
        """
        Perform sentiment analysis.
        
        Args:
            token_data: Token data from DexScreener
            coingecko_data: Data from CoinGecko
            social_data: External social media data (if available)
            price_changes: Recent price changes for market sentiment
            
        Returns:
            SentimentAnalysis object
        """
        analysis = SentimentAnalysis()
        
        # Extract social links
        twitter_url = token_data.get("twitter")
        telegram_url = token_data.get("telegram")
        discord_url = token_data.get("discord")
        
        # Analyze CoinGecko sentiment data if available
        if coingecko_data:
            cg_sentiment = self._analyze_coingecko_sentiment(coingecko_data)
            analysis.sentiment_score = cg_sentiment.get("score", 50.0)
            analysis.overall_sentiment = cg_sentiment.get("sentiment", "NEUTRAL")
            
            # Community data
            community_data = coingecko_data.get("community_data", {})
            if community_data:
                analysis.twitter_mentions = community_data.get("twitter_followers", 0)
                analysis.telegram_members = community_data.get("telegram_channel_user_count")
        
        # Analyze price action sentiment (market reaction)
        if price_changes:
            price_sentiment = self._analyze_price_sentiment(price_changes)
            # Blend with existing sentiment
            analysis.sentiment_score = (
                analysis.sentiment_score * 0.6 + price_sentiment * 0.4
            )
        
        # Analyze transaction sentiment from DexScreener
        txns = token_data.get("txns", {})
        if txns:
            txn_sentiment = self._analyze_transaction_sentiment(txns)
            analysis.sentiment_score = (
                analysis.sentiment_score * 0.7 + txn_sentiment * 0.3
            )
        
        # Determine community activity level
        analysis.community_activity = self._rate_community_activity(
            twitter_url, telegram_url, discord_url,
            analysis.twitter_mentions,
            analysis.telegram_members
        )
        
        # Determine overall sentiment
        analysis.overall_sentiment = self._determine_overall_sentiment(analysis.sentiment_score)
        
        # Set signal
        if analysis.sentiment_score >= 65:
            analysis.signal = "BULLISH"
        elif analysis.sentiment_score <= 35:
            analysis.signal = "BEARISH"
        else:
            analysis.signal = "NEUTRAL"
        
        # Generate summary
        analysis.summary = self._generate_summary(analysis)
        
        return analysis
    
    def _analyze_coingecko_sentiment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze CoinGecko sentiment data."""
        score = 50.0
        
        up_pct = data.get("sentiment_votes_up_percentage")
        down_pct = data.get("sentiment_votes_down_percentage")
        
        if up_pct is not None and down_pct is not None:
            # Convert sentiment percentages to score
            score = up_pct
        
        community_score = data.get("community_score")
        if community_score:
            score = (score + community_score * 10) / 2
        
        public_interest = data.get("public_interest_score")
        if public_interest:
            score = (score + public_interest * 10) / 2
        
        sentiment = "NEUTRAL"
        if score >= 65:
            sentiment = "POSITIVE"
        elif score <= 35:
            sentiment = "NEGATIVE"
        
        return {"score": score, "sentiment": sentiment}
    
    def _analyze_price_sentiment(self, price_changes: Dict[str, float]) -> float:
        """Derive sentiment from price action."""
        score = 50.0
        
        h1 = price_changes.get("h1", 0) or 0
        h6 = price_changes.get("h6", 0) or 0
        h24 = price_changes.get("h24", 0) or 0
        
        # Weight recent changes more heavily
        weighted_change = (h1 * 0.5) + (h6 * 0.3) + (h24 * 0.2)
        
        # Convert to 0-100 scale
        # +20% change = 100, -20% change = 0
        score = 50 + (weighted_change * 2.5)
        score = max(0, min(100, score))
        
        return score
    
    def _analyze_transaction_sentiment(self, txns: Dict[str, Any]) -> float:
        """Analyze buy/sell transaction sentiment."""
        score = 50.0
        
        # Get 24h transactions
        h24 = txns.get("h24", {})
        buys = h24.get("buys", 0) or 0
        sells = h24.get("sells", 0) or 0
        
        total = buys + sells
        if total > 0:
            buy_ratio = buys / total
            # Convert to 0-100 scale (0.5 = 50, 1.0 = 100, 0.0 = 0)
            score = buy_ratio * 100
        
        return score
    
    def _rate_community_activity(
        self,
        twitter: Optional[str],
        telegram: Optional[str],
        discord: Optional[str],
        twitter_followers: int = 0,
        telegram_members: Optional[int] = None
    ) -> str:
        """Rate community activity level."""
        # Count active channels
        channels = sum([
            1 if twitter else 0,
            1 if telegram else 0,
            1 if discord else 0
        ])
        
        # Check follower counts
        has_significant_following = (
            twitter_followers >= 1000 or
            (telegram_members and telegram_members >= 500)
        )
        
        if channels >= 3 and has_significant_following:
            return "very_active"
        elif channels >= 2 and has_significant_following:
            return "active"
        elif channels >= 2 or has_significant_following:
            return "moderate"
        elif channels >= 1:
            return "low"
        else:
            return "inactive"
    
    def _determine_overall_sentiment(self, score: float) -> str:
        """Determine overall sentiment label."""
        if score >= 70:
            return "POSITIVE"
        elif score >= 55:
            return "SLIGHTLY_POSITIVE"
        elif score <= 30:
            return "NEGATIVE"
        elif score <= 45:
            return "SLIGHTLY_NEGATIVE"
        else:
            return "NEUTRAL"
    
    def _generate_summary(self, analysis: SentimentAnalysis) -> str:
        """Generate human-readable sentiment summary."""
        points = []
        
        points.append(f"Overall sentiment: {analysis.overall_sentiment}")
        
        if analysis.community_activity:
            points.append(f"Community activity: {analysis.community_activity}")
        
        if analysis.twitter_mentions > 0:
            points.append(f"Twitter followers: {analysis.twitter_mentions:,}")
        
        if analysis.telegram_members:
            points.append(f"Telegram members: {analysis.telegram_members:,}")
        
        return ". ".join(points) if points else "Limited sentiment data available"
