"""
Data models for MuppinLLM analysis results.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime


class Verdict(str, Enum):
    """Market verdict enumeration."""
    EXTREMELY_BULLISH = "EXTREMELY_BULLISH"
    BULLISH = "BULLISH"
    SLIGHTLY_BULLISH = "SLIGHTLY_BULLISH"
    NEUTRAL = "NEUTRAL"
    SLIGHTLY_BEARISH = "SLIGHTLY_BEARISH"
    BEARISH = "BEARISH"
    EXTREMELY_BEARISH = "EXTREMELY_BEARISH"


@dataclass
class TokenData:
    """Basic token information from DEX and CoinGecko."""
    contract_address: str
    name: Optional[str] = None
    symbol: Optional[str] = None
    price_usd: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_1h: Optional[float] = None
    price_change_6h: Optional[float] = None
    volume_24h: Optional[float] = None
    volume_6h: Optional[float] = None
    volume_1h: Optional[float] = None
    liquidity_usd: Optional[float] = None
    fdv: Optional[float] = None
    market_cap: Optional[float] = None
    total_supply: Optional[float] = None
    circulating_supply: Optional[float] = None
    holders_count: Optional[int] = None
    pool_created_at: Optional[datetime] = None
    dex_name: Optional[str] = None
    pair_address: Optional[str] = None
    base_token: Optional[str] = None
    quote_token: Optional[str] = None
    
    # Historical price data for technical analysis
    price_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Social links
    website: Optional[str] = None
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    discord: Optional[str] = None


@dataclass
class TechnicalAnalysis:
    """Technical analysis indicators and signals."""
    # Trend indicators
    rsi_14: Optional[float] = None
    rsi_signal: Optional[str] = None  # oversold, neutral, overbought
    
    # Moving averages
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    
    # MACD
    macd_line: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    macd_trend: Optional[str] = None  # bullish, bearish, neutral
    
    # Bollinger Bands
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None
    bb_position: Optional[str] = None  # above_upper, near_upper, middle, near_lower, below_lower
    
    # Volume analysis
    volume_trend: Optional[str] = None  # increasing, decreasing, stable
    volume_ma_20: Optional[float] = None
    
    # Price action
    support_level: Optional[float] = None
    resistance_level: Optional[float] = None
    trend_direction: Optional[str] = None  # uptrend, downtrend, sideways
    
    # Overall technical score (0-100)
    score: float = 50.0
    signal: str = "NEUTRAL"  # BULLISH, BEARISH, NEUTRAL
    
    # Analysis summary
    summary: str = ""


@dataclass
class FundamentalAnalysis:
    """Fundamental analysis of the token."""
    # Liquidity metrics
    liquidity_usd: Optional[float] = None
    liquidity_rating: Optional[str] = None  # excellent, good, moderate, low, very_low
    
    # Volume metrics
    volume_24h: Optional[float] = None
    volume_to_liquidity_ratio: Optional[float] = None
    volume_rating: Optional[str] = None  # high, moderate, low
    
    # Token distribution
    holders_count: Optional[int] = None
    top_holders_concentration: Optional[float] = None  # percentage held by top 10
    holder_rating: Optional[str] = None  # well_distributed, moderate, concentrated
    
    # Market metrics
    fdv: Optional[float] = None
    market_cap: Optional[float] = None
    fdv_to_mcap_ratio: Optional[float] = None
    
    # Age and maturity
    token_age_days: Optional[int] = None
    maturity_rating: Optional[str] = None  # new, young, established, mature
    
    # DEX presence
    dex_listings: List[str] = field(default_factory=list)
    total_pools: int = 0
    
    # Overall fundamental score (0-100)
    score: float = 50.0
    signal: str = "NEUTRAL"
    
    # Analysis summary
    summary: str = ""


@dataclass
class SentimentAnalysis:
    """Social media and news sentiment analysis."""
    # Overall sentiment
    overall_sentiment: str = "NEUTRAL"  # POSITIVE, NEGATIVE, NEUTRAL, MIXED
    sentiment_score: float = 50.0  # 0-100, 50 is neutral
    
    # Twitter/X analysis
    twitter_mentions: int = 0
    twitter_sentiment: Optional[str] = None
    twitter_engagement: Optional[float] = None
    trending_hashtags: List[str] = field(default_factory=list)
    
    # News analysis
    recent_news_count: int = 0
    news_sentiment: Optional[str] = None
    key_news_topics: List[str] = field(default_factory=list)
    
    # Community metrics
    community_activity: Optional[str] = None  # very_active, active, moderate, low, inactive
    telegram_members: Optional[int] = None
    discord_members: Optional[int] = None
    
    # Influencer activity
    influencer_mentions: int = 0
    notable_mentions: List[str] = field(default_factory=list)
    
    # Overall signal
    signal: str = "NEUTRAL"
    
    # Analysis summary
    summary: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result from MuppinLLM."""
    # Token information
    token: TokenData
    
    # Analysis components
    technical: TechnicalAnalysis
    fundamental: FundamentalAnalysis
    sentiment: SentimentAnalysis
    
    # Final verdict
    verdict: Verdict = Verdict.NEUTRAL
    strength: int = 50  # 1-100, how confident is the verdict
    
    # Weighted scores
    technical_weight: float = 0.4
    fundamental_weight: float = 0.35
    sentiment_weight: float = 0.25
    
    # Combined score (0-100)
    combined_score: float = 50.0
    
    # AI-generated analysis
    ai_summary: str = ""
    ai_recommendation: str = ""
    risk_factors: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    
    # Metadata
    analyzed_at: datetime = field(default_factory=datetime.utcnow)
    analysis_version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis result to dictionary."""
        return {
            "token": {
                "contract_address": self.token.contract_address,
                "name": self.token.name,
                "symbol": self.token.symbol,
                "price_usd": self.token.price_usd,
                "price_change_24h": self.token.price_change_24h,
                "volume_24h": self.token.volume_24h,
                "liquidity_usd": self.token.liquidity_usd,
                "fdv": self.token.fdv,
                "market_cap": self.token.market_cap,
            },
            "verdict": self.verdict.value,
            "strength": self.strength,
            "combined_score": self.combined_score,
            "technical": {
                "score": self.technical.score,
                "signal": self.technical.signal,
                "rsi_14": self.technical.rsi_14,
                "macd_trend": self.technical.macd_trend,
                "trend_direction": self.technical.trend_direction,
                "summary": self.technical.summary,
            },
            "fundamental": {
                "score": self.fundamental.score,
                "signal": self.fundamental.signal,
                "liquidity_rating": self.fundamental.liquidity_rating,
                "volume_rating": self.fundamental.volume_rating,
                "summary": self.fundamental.summary,
            },
            "sentiment": {
                "score": self.sentiment.sentiment_score,
                "signal": self.sentiment.signal,
                "overall_sentiment": self.sentiment.overall_sentiment,
                "summary": self.sentiment.summary,
            },
            "ai_summary": self.ai_summary,
            "ai_recommendation": self.ai_recommendation,
            "risk_factors": self.risk_factors,
            "opportunities": self.opportunities,
            "analyzed_at": self.analyzed_at.isoformat(),
        }
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        bull_emoji = "🐂" if "BULLISH" in self.verdict.value else "🐻"
        price_str = f"${self.token.price_usd:.8f}" if self.token.price_usd else "N/A"
        change_str = f"{self.token.price_change_24h:.2f}" if self.token.price_change_24h else "0"
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  MUPPIN ANALYSIS REPORT - {self.token.symbol or 'UNKNOWN'}
╠══════════════════════════════════════════════════════════════╣
║  Contract: {self.token.contract_address[:20]}...
║  Price: {price_str}
║  24h Change: {change_str}%
╠══════════════════════════════════════════════════════════════╣
║  {bull_emoji} VERDICT: {self.verdict.value}
║  Strength: {self.strength}/100
║  Combined Score: {self.combined_score:.1f}/100
╠══════════════════════════════════════════════════════════════╣
║  Technical Score: {self.technical.score:.1f}/100 ({self.technical.signal})
║  Fundamental Score: {self.fundamental.score:.1f}/100 ({self.fundamental.signal})
║  Sentiment Score: {self.sentiment.sentiment_score:.1f}/100 ({self.sentiment.signal})
╠══════════════════════════════════════════════════════════════╣
║  AI SUMMARY:
║  {self.ai_summary[:60]}...
╚══════════════════════════════════════════════════════════════╝
"""
