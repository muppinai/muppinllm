"""
Fundamental analysis module for MuppinLLM.
Analyzes token fundamentals like liquidity, volume, and holder distribution.
"""
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone
from ..models import FundamentalAnalysis


class FundamentalAnalyzer:
    """
    Fundamental analysis for crypto tokens.
    
    Analyzes:
    - Liquidity metrics
    - Volume analysis
    - Token distribution
    - Market metrics (FDV, market cap)
    - Token age and maturity
    - DEX presence
    """
    
    # Thresholds for various ratings
    LIQUIDITY_THRESHOLDS = {
        "excellent": 1_000_000,  # $1M+
        "good": 100_000,         # $100K+
        "moderate": 10_000,      # $10K+
        "low": 1_000,            # $1K+
        "very_low": 0            # Below $1K
    }
    
    VOLUME_THRESHOLDS = {
        "high": 100_000,     # $100K+ daily
        "moderate": 10_000,  # $10K+ daily
        "low": 0             # Below $10K
    }
    
    def __init__(self):
        """Initialize the fundamental analyzer."""
        pass
    
    def analyze(
        self,
        token_data: Dict[str, Any],
        coingecko_data: Optional[Dict[str, Any]] = None
    ) -> FundamentalAnalysis:
        """
        Perform comprehensive fundamental analysis.
        
        Args:
            token_data: Token data from DexScreener
            coingecko_data: Additional data from CoinGecko
            
        Returns:
            FundamentalAnalysis object
        """
        analysis = FundamentalAnalysis()
        
        # Liquidity analysis
        liquidity = token_data.get("liquidity_usd") or 0
        analysis.liquidity_usd = liquidity
        analysis.liquidity_rating = self._rate_liquidity(liquidity)
        
        # Volume analysis
        volume_24h = token_data.get("volume_24h") or 0
        analysis.volume_24h = volume_24h
        analysis.volume_rating = self._rate_volume(volume_24h)
        
        if liquidity > 0:
            analysis.volume_to_liquidity_ratio = volume_24h / liquidity
        
        # Market metrics
        analysis.fdv = token_data.get("fdv")
        analysis.market_cap = token_data.get("market_cap")
        
        if analysis.fdv and analysis.market_cap and analysis.market_cap > 0:
            analysis.fdv_to_mcap_ratio = analysis.fdv / analysis.market_cap
        
        # Token age
        created_at = token_data.get("pair_created_at")
        if created_at:
            analysis.token_age_days = self._calculate_age_days(created_at)
            analysis.maturity_rating = self._rate_maturity(analysis.token_age_days)
        
        # DEX presence
        all_pairs = token_data.get("all_pairs", [])
        analysis.total_pools = len(all_pairs)
        analysis.dex_listings = list(set(
            pair.get("dexId", "unknown") 
            for pair in all_pairs
        ))
        
        # Holder analysis from CoinGecko if available
        if coingecko_data:
            community_data = coingecko_data.get("community_data", {})
            if community_data:
                analysis.telegram_members = community_data.get("telegram_channel_user_count")
            
            market_data = coingecko_data.get("market_data", {})
            if market_data:
                analysis.holders_count = market_data.get("total_supply")
        
        # Calculate overall score
        analysis.score, analysis.signal = self._calculate_fundamental_score(analysis)
        
        # Generate summary
        analysis.summary = self._generate_summary(analysis)
        
        return analysis
    
    def _rate_liquidity(self, liquidity: float) -> str:
        """Rate liquidity level."""
        for rating, threshold in self.LIQUIDITY_THRESHOLDS.items():
            if liquidity >= threshold:
                return rating
        return "very_low"
    
    def _rate_volume(self, volume: float) -> str:
        """Rate volume level."""
        for rating, threshold in self.VOLUME_THRESHOLDS.items():
            if volume >= threshold:
                return rating
        return "low"
    
    def _calculate_age_days(self, created_at: Any) -> int:
        """Calculate token age in days."""
        try:
            if isinstance(created_at, (int, float)):
                # Unix timestamp in milliseconds
                created_datetime = datetime.fromtimestamp(created_at / 1000, tz=timezone.utc)
            elif isinstance(created_at, str):
                created_datetime = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            else:
                return 0
            
            now = datetime.now(timezone.utc)
            delta = now - created_datetime
            return max(0, delta.days)
        except Exception:
            return 0
    
    def _rate_maturity(self, age_days: int) -> str:
        """Rate token maturity based on age."""
        if age_days >= 365:
            return "mature"
        elif age_days >= 90:
            return "established"
        elif age_days >= 30:
            return "young"
        else:
            return "new"
    
    def _calculate_fundamental_score(
        self,
        analysis: FundamentalAnalysis
    ) -> Tuple[float, str]:
        """Calculate overall fundamental score (0-100)."""
        score = 50.0
        
        # Liquidity contribution (-20 to +20)
        liquidity_scores = {
            "excellent": 20,
            "good": 10,
            "moderate": 0,
            "low": -10,
            "very_low": -20
        }
        score += liquidity_scores.get(analysis.liquidity_rating or "moderate", 0)
        
        # Volume contribution (-15 to +15)
        volume_scores = {
            "high": 15,
            "moderate": 5,
            "low": -10
        }
        score += volume_scores.get(analysis.volume_rating or "moderate", 0)
        
        # Volume to liquidity ratio (healthy is 0.1 - 2.0)
        if analysis.volume_to_liquidity_ratio:
            ratio = analysis.volume_to_liquidity_ratio
            if 0.1 <= ratio <= 2.0:
                score += 5
            elif ratio > 5.0:  # Possible wash trading
                score -= 5
            elif ratio < 0.01:  # Very low activity
                score -= 5
        
        # Maturity contribution (-5 to +10)
        maturity_scores = {
            "mature": 10,
            "established": 5,
            "young": 0,
            "new": -5
        }
        score += maturity_scores.get(analysis.maturity_rating or "young", 0)
        
        # DEX presence contribution (0 to +10)
        if analysis.total_pools >= 5:
            score += 10
        elif analysis.total_pools >= 3:
            score += 5
        elif analysis.total_pools >= 2:
            score += 2
        
        # Clamp score
        score = max(0, min(100, score))
        
        # Determine signal
        if score >= 65:
            signal = "BULLISH"
        elif score <= 35:
            signal = "BEARISH"
        else:
            signal = "NEUTRAL"
        
        return round(score, 1), signal
    
    def _generate_summary(self, analysis: FundamentalAnalysis) -> str:
        """Generate human-readable fundamental analysis summary."""
        points = []
        
        if analysis.liquidity_usd:
            points.append(f"Liquidity ${analysis.liquidity_usd:,.0f} ({analysis.liquidity_rating})")
        
        if analysis.volume_24h:
            points.append(f"24h volume ${analysis.volume_24h:,.0f} ({analysis.volume_rating})")
        
        if analysis.maturity_rating:
            age_str = f"{analysis.token_age_days} days" if analysis.token_age_days else "unknown"
            points.append(f"Token age: {age_str} ({analysis.maturity_rating})")
        
        if analysis.total_pools > 0:
            points.append(f"Listed on {analysis.total_pools} pools across {len(analysis.dex_listings)} DEXs")
        
        if analysis.fdv:
            points.append(f"FDV ${analysis.fdv:,.0f}")
        
        return ". ".join(points) if points else "Insufficient data for fundamental analysis"
