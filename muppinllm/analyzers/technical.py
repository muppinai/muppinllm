"""
Technical analysis module for MuppinLLM.
Calculates various technical indicators and signals.
"""
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from ..models import TechnicalAnalysis


class TechnicalAnalyzer:
    """
    Technical analysis calculator for crypto tokens.
    
    Calculates:
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence)
    - Bollinger Bands
    - Moving Averages (SMA, EMA)
    - Support/Resistance levels
    - Volume analysis
    """
    
    def __init__(self):
        """Initialize the technical analyzer."""
        pass
    
    def analyze(
        self,
        prices: List[float],
        volumes: Optional[List[float]] = None,
        current_price: Optional[float] = None,
        price_changes: Optional[Dict[str, float]] = None
    ) -> TechnicalAnalysis:
        """
        Perform comprehensive technical analysis.
        
        Args:
            prices: Historical price data (oldest to newest)
            volumes: Historical volume data
            current_price: Current token price
            price_changes: Dict with h1, h6, h24 price changes
            
        Returns:
            TechnicalAnalysis object with all indicators
        """
        analysis = TechnicalAnalysis()
        
        if not prices or len(prices) < 2:
            analysis.summary = "Insufficient price data for technical analysis"
            return analysis
        
        prices_arr = np.array(prices, dtype=float)
        
        # Calculate RSI
        if len(prices_arr) >= 14:
            analysis.rsi_14 = self._calculate_rsi(prices_arr, 14)
            analysis.rsi_signal = self._interpret_rsi(analysis.rsi_14)
        
        # Calculate Moving Averages
        if len(prices_arr) >= 20:
            analysis.sma_20 = self._calculate_sma(prices_arr, 20)
        if len(prices_arr) >= 50:
            analysis.sma_50 = self._calculate_sma(prices_arr, 50)
        if len(prices_arr) >= 12:
            analysis.ema_12 = self._calculate_ema(prices_arr, 12)
        if len(prices_arr) >= 26:
            analysis.ema_26 = self._calculate_ema(prices_arr, 26)
        
        # Calculate MACD
        if len(prices_arr) >= 26:
            macd_line, signal_line, histogram = self._calculate_macd(prices_arr)
            analysis.macd_line = macd_line
            analysis.macd_signal = signal_line
            analysis.macd_histogram = histogram
            analysis.macd_trend = self._interpret_macd(macd_line, signal_line, histogram)
        
        # Calculate Bollinger Bands
        if len(prices_arr) >= 20:
            upper, middle, lower = self._calculate_bollinger_bands(prices_arr)
            analysis.bb_upper = upper
            analysis.bb_middle = middle
            analysis.bb_lower = lower
            if current_price:
                analysis.bb_position = self._interpret_bb_position(current_price, upper, middle, lower)
        
        # Volume analysis
        if volumes and len(volumes) >= 20:
            volumes_arr = np.array(volumes, dtype=float)
            analysis.volume_ma_20 = self._calculate_sma(volumes_arr, 20)
            analysis.volume_trend = self._analyze_volume_trend(volumes_arr)
        
        # Support and Resistance
        if len(prices_arr) >= 10:
            analysis.support_level, analysis.resistance_level = self._find_support_resistance(prices_arr)
        
        # Trend direction
        analysis.trend_direction = self._determine_trend(prices_arr, price_changes)
        
        # Calculate overall score
        analysis.score, analysis.signal = self._calculate_technical_score(analysis, price_changes)
        
        # Generate summary
        analysis.summary = self._generate_summary(analysis)
        
        return analysis
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        """Calculate Relative Strength Index."""
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    def _interpret_rsi(self, rsi: float) -> str:
        """Interpret RSI value."""
        if rsi >= 70:
            return "overbought"
        elif rsi <= 30:
            return "oversold"
        else:
            return "neutral"
    
    def _calculate_sma(self, data: np.ndarray, period: int) -> float:
        """Calculate Simple Moving Average."""
        if len(data) < period:
            return float(np.mean(data))
        return float(np.mean(data[-period:]))
    
    def _calculate_ema(self, data: np.ndarray, period: int) -> float:
        """Calculate Exponential Moving Average."""
        multiplier = 2 / (period + 1)
        ema = data[0]
        
        for price in data[1:]:
            ema = (price - ema) * multiplier + ema
        
        return float(ema)
    
    def _calculate_macd(
        self,
        prices: np.ndarray,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Tuple[float, float, float]:
        """Calculate MACD indicator."""
        ema_fast = self._calculate_ema(prices, fast)
        ema_slow = self._calculate_ema(prices, slow)
        
        macd_line = ema_fast - ema_slow
        
        # Calculate signal line (9-period EMA of MACD)
        # Simplified: use current MACD as approximation
        signal_line = macd_line * 0.9  # Approximation
        
        histogram = macd_line - signal_line
        
        return float(macd_line), float(signal_line), float(histogram)
    
    def _interpret_macd(self, macd_line: float, signal_line: float, histogram: float) -> str:
        """Interpret MACD signals."""
        if macd_line > signal_line and histogram > 0:
            return "bullish"
        elif macd_line < signal_line and histogram < 0:
            return "bearish"
        else:
            return "neutral"
    
    def _calculate_bollinger_bands(
        self,
        prices: np.ndarray,
        period: int = 20,
        std_dev: float = 2.0
    ) -> Tuple[float, float, float]:
        """Calculate Bollinger Bands."""
        sma = self._calculate_sma(prices, period)
        std = float(np.std(prices[-period:]))
        
        upper = sma + (std_dev * std)
        lower = sma - (std_dev * std)
        
        return upper, sma, lower
    
    def _interpret_bb_position(
        self,
        price: float,
        upper: float,
        middle: float,
        lower: float
    ) -> str:
        """Interpret price position relative to Bollinger Bands."""
        if price > upper:
            return "above_upper"
        elif price > middle + (upper - middle) * 0.5:
            return "near_upper"
        elif price < lower:
            return "below_lower"
        elif price < middle - (middle - lower) * 0.5:
            return "near_lower"
        else:
            return "middle"
    
    def _analyze_volume_trend(self, volumes: np.ndarray) -> str:
        """Analyze volume trend."""
        recent = np.mean(volumes[-5:])
        older = np.mean(volumes[-20:-5]) if len(volumes) >= 20 else np.mean(volumes[:-5])
        
        if recent > older * 1.2:
            return "increasing"
        elif recent < older * 0.8:
            return "decreasing"
        else:
            return "stable"
    
    def _find_support_resistance(self, prices: np.ndarray) -> Tuple[float, float]:
        """Find basic support and resistance levels."""
        recent_prices = prices[-20:]
        
        support = float(np.min(recent_prices))
        resistance = float(np.max(recent_prices))
        
        return support, resistance
    
    def _determine_trend(
        self,
        prices: np.ndarray,
        price_changes: Optional[Dict[str, float]] = None
    ) -> str:
        """Determine overall trend direction."""
        if price_changes:
            h24 = price_changes.get("h24", 0) or 0
            h6 = price_changes.get("h6", 0) or 0
            h1 = price_changes.get("h1", 0) or 0
            
            # Weight recent changes more
            weighted_change = (h1 * 0.4) + (h6 * 0.35) + (h24 * 0.25)
            
            if weighted_change > 5:
                return "uptrend"
            elif weighted_change < -5:
                return "downtrend"
        
        # Fallback to price array analysis
        if len(prices) >= 10:
            recent_avg = np.mean(prices[-5:])
            older_avg = np.mean(prices[-10:-5])
            
            if recent_avg > older_avg * 1.05:
                return "uptrend"
            elif recent_avg < older_avg * 0.95:
                return "downtrend"
        
        return "sideways"
    
    def _calculate_technical_score(
        self,
        analysis: TechnicalAnalysis,
        price_changes: Optional[Dict[str, float]] = None
    ) -> Tuple[float, str]:
        """Calculate overall technical score (0-100)."""
        score = 50.0  # Start neutral
        
        # RSI contribution (-15 to +15)
        if analysis.rsi_14:
            if analysis.rsi_14 < 30:
                score += 15  # Oversold = bullish
            elif analysis.rsi_14 > 70:
                score -= 15  # Overbought = bearish
            elif analysis.rsi_14 < 45:
                score += 5
            elif analysis.rsi_14 > 55:
                score -= 5
        
        # MACD contribution (-15 to +15)
        if analysis.macd_trend:
            if analysis.macd_trend == "bullish":
                score += 15
            elif analysis.macd_trend == "bearish":
                score -= 15
        
        # Trend contribution (-10 to +10)
        if analysis.trend_direction == "uptrend":
            score += 10
        elif analysis.trend_direction == "downtrend":
            score -= 10
        
        # Bollinger Bands contribution (-10 to +10)
        if analysis.bb_position:
            if analysis.bb_position == "below_lower":
                score += 10  # Potential bounce
            elif analysis.bb_position == "above_upper":
                score -= 10  # Potential pullback
            elif analysis.bb_position == "near_lower":
                score += 5
            elif analysis.bb_position == "near_upper":
                score -= 5
        
        # Volume contribution (-5 to +5)
        if analysis.volume_trend:
            if analysis.volume_trend == "increasing" and analysis.trend_direction == "uptrend":
                score += 5
            elif analysis.volume_trend == "increasing" and analysis.trend_direction == "downtrend":
                score -= 5
        
        # Price change contribution
        if price_changes:
            h24 = price_changes.get("h24", 0) or 0
            if h24 > 10:
                score += 5
            elif h24 < -10:
                score -= 5
        
        # Clamp score to 0-100
        score = max(0, min(100, score))
        
        # Determine signal
        if score >= 65:
            signal = "BULLISH"
        elif score <= 35:
            signal = "BEARISH"
        else:
            signal = "NEUTRAL"
        
        return round(score, 1), signal
    
    def _generate_summary(self, analysis: TechnicalAnalysis) -> str:
        """Generate human-readable technical analysis summary."""
        points = []
        
        if analysis.rsi_14:
            points.append(f"RSI at {analysis.rsi_14:.1f} ({analysis.rsi_signal})")
        
        if analysis.macd_trend:
            points.append(f"MACD showing {analysis.macd_trend} momentum")
        
        if analysis.trend_direction:
            points.append(f"Price in {analysis.trend_direction}")
        
        if analysis.volume_trend:
            points.append(f"Volume {analysis.volume_trend}")
        
        if analysis.bb_position:
            bb_desc = {
                "above_upper": "above upper band (overbought zone)",
                "near_upper": "near upper band",
                "middle": "at middle band",
                "near_lower": "near lower band",
                "below_lower": "below lower band (oversold zone)"
            }
            points.append(f"Price {bb_desc.get(analysis.bb_position, analysis.bb_position)}")
        
        return ". ".join(points) if points else "Insufficient data for detailed analysis"
