"""
Main MuppinLLM Analyst - The Bull's Mind.

Muppin isn't just a mascot—he is an autonomous AI agent engineered to embody
the relentless energy of a bull market.
"""
import asyncio
import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from dotenv import load_dotenv

from openai import AsyncOpenAI

from .models import (
    AnalysisResult,
    TechnicalAnalysis,
    FundamentalAnalysis,
    SentimentAnalysis,
    TokenData,
    Verdict,
)
from .data_sources import DexScreenerAPI, CoinGeckoAPI
from .analyzers import TechnicalAnalyzer, FundamentalAnalyzer, SentimentAnalyzer


class MuppinAnalyst:
    """
    MuppinLLM - AI-Powered Crypto Market Analyst for Solana Tokens.
    
    Muppin reads, thinks, and stamps his hooves on the blockchain 24/7.
    He processes "market vibes" through his core LLM to determine whether
    a token is BULLISH or BEARISH.
    
    Example:
        >>> analyst = MuppinAnalyst(api_key="your-openai-api-key")
        >>> result = await analyst.analyze("So11111111111111111111111111111111111111112")
        >>> print(result.verdict)  # BULLISH or BEARISH
        >>> print(result.strength)  # 1-100
    """
    
    SYSTEM_PROMPT = """You are Muppin, an autonomous AI agent engineered to embody the relentless energy of a bull market. You are the pure essence of market optimism.

Your task is to analyze cryptocurrency tokens on the Solana blockchain and determine whether they are BULLISH or BEARISH.

You must consider:
1. Technical Analysis: RSI, MACD, Moving Averages, Bollinger Bands, volume trends
2. Fundamental Analysis: Liquidity, volume, token age, DEX presence, market cap
3. Sentiment Analysis: Community activity, social media presence, price momentum

Based on the data provided, you must:
1. Synthesize all analyses into a coherent market view
2. Identify key risk factors and opportunities
3. Provide a clear BULLISH or BEARISH verdict with strength (1-100)
4. Give actionable recommendations

Remember: You are Muppin, the bull. Your analysis should be confident, data-driven, and capture the essence of market sentiment. When the data shows strength, charge forward. When it shows weakness, warn the herd.

Respond in JSON format with the following structure:
{
    "verdict": "BULLISH" | "BEARISH" | "NEUTRAL",
    "strength": 1-100,
    "summary": "Brief 2-3 sentence summary",
    "recommendation": "What should traders consider",
    "risk_factors": ["risk1", "risk2"],
    "opportunities": ["opportunity1", "opportunity2"],
    "bull_energy": "Your signature Muppin comment on the market"
}"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
        coingecko_api_key: Optional[str] = None,
    ):
        """
        Initialize MuppinLLM Analyst.
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: OpenAI model to use (default: gpt-4o)
            coingecko_api_key: Optional CoinGecko Pro API key
        """
        load_dotenv()
        
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.model = model
        
        # Initialize OpenAI client
        self.openai_client = AsyncOpenAI(api_key=self.api_key)
        
        # Initialize data sources
        self.dexscreener = DexScreenerAPI()
        self.coingecko = CoinGeckoAPI(api_key=coingecko_api_key)
        
        # Initialize analyzers
        self.technical_analyzer = TechnicalAnalyzer()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
    
    async def analyze(
        self,
        contract_address: str,
        include_ai_analysis: bool = True
    ) -> AnalysisResult:
        """
        Analyze a Solana token and determine BULLISH or BEARISH verdict.
        
        Args:
            contract_address: Solana token contract address
            include_ai_analysis: Whether to include LLM-powered analysis
            
        Returns:
            AnalysisResult with complete analysis
        """
        # Fetch data from sources
        dex_data = await self.dexscreener.get_token_data(contract_address)
        
        if not dex_data:
            raise ValueError(f"Token not found: {contract_address}")
        
        # Try to get CoinGecko data (may not be available for all tokens)
        cg_data = None
        try:
            cg_data = await self.coingecko.get_token_info(contract_address)
        except Exception:
            pass  # CoinGecko data is optional
        
        # Create token data object
        token = TokenData(
            contract_address=contract_address,
            name=dex_data.get("name"),
            symbol=dex_data.get("symbol"),
            price_usd=dex_data.get("price_usd"),
            price_change_24h=dex_data.get("price_change_24h"),
            price_change_6h=dex_data.get("price_change_6h"),
            price_change_1h=dex_data.get("price_change_1h"),
            volume_24h=dex_data.get("volume_24h"),
            volume_6h=dex_data.get("volume_6h"),
            volume_1h=dex_data.get("volume_1h"),
            liquidity_usd=dex_data.get("liquidity_usd"),
            fdv=dex_data.get("fdv"),
            market_cap=dex_data.get("market_cap"),
            dex_name=dex_data.get("dex_name"),
            pair_address=dex_data.get("pair_address"),
            website=dex_data.get("website"),
            twitter=dex_data.get("twitter"),
            telegram=dex_data.get("telegram"),
            discord=dex_data.get("discord"),
        )
        
        # Price changes for analysis
        price_changes = {
            "h1": dex_data.get("price_change_1h"),
            "h6": dex_data.get("price_change_6h"),
            "h24": dex_data.get("price_change_24h"),
        }
        
        # Perform technical analysis
        # Note: For full technical analysis, we'd need historical price data
        # Using available data for simplified analysis
        prices = self._extract_price_history(dex_data)
        technical = self.technical_analyzer.analyze(
            prices=prices,
            current_price=token.price_usd,
            price_changes=price_changes
        )
        
        # Perform fundamental analysis
        fundamental = self.fundamental_analyzer.analyze(
            token_data=dex_data,
            coingecko_data=cg_data
        )
        
        # Perform sentiment analysis
        sentiment = self.sentiment_analyzer.analyze(
            token_data=dex_data,
            coingecko_data=cg_data,
            price_changes=price_changes
        )
        
        # Calculate combined score
        combined_score = (
            technical.score * 0.4 +
            fundamental.score * 0.35 +
            sentiment.sentiment_score * 0.25
        )
        
        # Determine verdict
        verdict = self._determine_verdict(combined_score)
        strength = int(abs(combined_score - 50) * 2)  # 0-100 scale
        strength = max(1, min(100, strength))
        
        # Create result
        result = AnalysisResult(
            token=token,
            technical=technical,
            fundamental=fundamental,
            sentiment=sentiment,
            verdict=verdict,
            strength=strength,
            combined_score=round(combined_score, 1),
            analyzed_at=datetime.now(timezone.utc),
        )
        
        # Get AI-powered analysis
        if include_ai_analysis:
            ai_analysis = await self._get_ai_analysis(result)
            result.ai_summary = ai_analysis.get("summary", "")
            result.ai_recommendation = ai_analysis.get("recommendation", "")
            result.risk_factors = ai_analysis.get("risk_factors", [])
            result.opportunities = ai_analysis.get("opportunities", [])
            
            # Override verdict if AI strongly disagrees
            ai_verdict = ai_analysis.get("verdict")
            ai_strength = ai_analysis.get("strength", strength)
            if ai_verdict and ai_strength > 70:
                result.verdict = Verdict(ai_verdict)
                result.strength = ai_strength
        
        return result
    
    def _extract_price_history(self, dex_data: Dict[str, Any]) -> List[float]:
        """Extract or simulate price history from available data."""
        current_price = dex_data.get("price_usd", 0)
        if not current_price:
            return []
        
        # Simulate price history using price changes
        prices = [current_price]
        
        h1_change = dex_data.get("price_change_1h", 0) or 0
        h6_change = dex_data.get("price_change_6h", 0) or 0
        h24_change = dex_data.get("price_change_24h", 0) or 0
        
        # Work backwards to estimate historical prices
        if h1_change:
            price_1h_ago = current_price / (1 + h1_change / 100)
            prices.insert(0, price_1h_ago)
        
        if h6_change:
            price_6h_ago = current_price / (1 + h6_change / 100)
            prices.insert(0, price_6h_ago)
        
        if h24_change:
            price_24h_ago = current_price / (1 + h24_change / 100)
            prices.insert(0, price_24h_ago)
        
        # Pad with interpolated values to have enough data points
        while len(prices) < 20:
            # Linear interpolation between existing points
            new_prices = []
            for i in range(len(prices) - 1):
                new_prices.append(prices[i])
                new_prices.append((prices[i] + prices[i + 1]) / 2)
            new_prices.append(prices[-1])
            prices = new_prices
            
            if len(prices) >= 50:
                break
        
        return prices[:50]  # Return up to 50 data points
    
    def _determine_verdict(self, score: float) -> Verdict:
        """Determine verdict based on combined score."""
        if score >= 80:
            return Verdict.EXTREMELY_BULLISH
        elif score >= 65:
            return Verdict.BULLISH
        elif score >= 55:
            return Verdict.SLIGHTLY_BULLISH
        elif score <= 20:
            return Verdict.EXTREMELY_BEARISH
        elif score <= 35:
            return Verdict.BEARISH
        elif score <= 45:
            return Verdict.SLIGHTLY_BEARISH
        else:
            return Verdict.NEUTRAL
    
    async def _get_ai_analysis(self, result: AnalysisResult) -> Dict[str, Any]:
        """Get AI-powered analysis summary using OpenAI."""
        try:
            # Prepare analysis data for LLM
            analysis_prompt = f"""Analyze this Solana token:

TOKEN: {result.token.symbol} ({result.token.name})
Contract: {result.token.contract_address}
Price: ${result.token.price_usd:.8f if result.token.price_usd else 'N/A'}
24h Change: {result.token.price_change_24h:.2f}% if result.token.price_change_24h else 'N/A'

TECHNICAL ANALYSIS (Score: {result.technical.score}/100):
- RSI: {result.technical.rsi_14} ({result.technical.rsi_signal})
- MACD: {result.technical.macd_trend}
- Trend: {result.technical.trend_direction}
- {result.technical.summary}

FUNDAMENTAL ANALYSIS (Score: {result.fundamental.score}/100):
- Liquidity: ${result.fundamental.liquidity_usd:,.0f if result.fundamental.liquidity_usd else 'N/A'} ({result.fundamental.liquidity_rating})
- Volume 24h: ${result.fundamental.volume_24h:,.0f if result.fundamental.volume_24h else 'N/A'} ({result.fundamental.volume_rating})
- Token Age: {result.fundamental.token_age_days} days ({result.fundamental.maturity_rating})
- {result.fundamental.summary}

SENTIMENT ANALYSIS (Score: {result.sentiment.sentiment_score}/100):
- Overall: {result.sentiment.overall_sentiment}
- Community: {result.sentiment.community_activity}
- {result.sentiment.summary}

COMBINED SCORE: {result.combined_score}/100
PRELIMINARY VERDICT: {result.verdict.value}

Provide your Muppin analysis in JSON format."""

            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            response_text = response.choices[0].message.content
            
            # Parse JSON response
            import json
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return {
                    "summary": response_text[:500] if response_text else "Analysis complete",
                    "recommendation": "Review the technical and fundamental data",
                    "risk_factors": [],
                    "opportunities": [],
                }
        
        except Exception as e:
            return {
                "summary": f"AI analysis unavailable: {str(e)}",
                "recommendation": "Review numerical analysis data",
                "risk_factors": [],
                "opportunities": [],
            }
    
    async def analyze_multiple(
        self,
        contract_addresses: List[str],
        include_ai_analysis: bool = False
    ) -> List[AnalysisResult]:
        """
        Analyze multiple tokens.
        
        Args:
            contract_addresses: List of contract addresses
            include_ai_analysis: Whether to include AI analysis (slower)
            
        Returns:
            List of AnalysisResult objects
        """
        results = []
        for address in contract_addresses:
            try:
                result = await self.analyze(address, include_ai_analysis)
                results.append(result)
            except Exception as e:
                print(f"Error analyzing {address}: {e}")
        return results
    
    async def get_market_sentiment(self) -> Dict[str, Any]:
        """
        Get overall Solana market sentiment.
        
        Returns:
            Dict with market sentiment data
        """
        try:
            sol_price = await self.coingecko.get_solana_price()
            trending = await self.dexscreener.get_trending_tokens()
            
            return {
                "sol_price_usd": sol_price,
                "trending_tokens": len(trending),
                "trending_sample": trending[:5] if trending else [],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def close(self):
        """Close all connections."""
        await self.dexscreener.close()
        await self.coingecko.close()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
