"""
MuppinLLM - AI-Powered Crypto Market Analyst for Solana Tokens

Muppin isn't just a mascot—he is an autonomous AI agent engineered to embody
the relentless energy of a bull market. This package provides AI-powered
analysis for Solana tokens using technical, fundamental, and sentiment analysis.

Example:
    >>> from muppinllm import MuppinAnalyst
    >>> analyst = MuppinAnalyst(api_key="your-emergent-llm-key")
    >>> result = await analyst.analyze("TokenContractAddress")
    >>> print(result.verdict)  # BULLISH or BEARISH
    >>> print(result.strength)  # 1-100
"""

__version__ = "1.0.0"
__author__ = "Muppin Team"
__email__ = "team@muppin.fun"
__url__ = "https://muppin.fun"

from .analyst import MuppinAnalyst
from .models import (
    AnalysisResult,
    TechnicalAnalysis,
    FundamentalAnalysis,
    SentimentAnalysis,
    TokenData,
    Verdict,
)

__all__ = [
    "MuppinAnalyst",
    "AnalysisResult",
    "TechnicalAnalysis",
    "FundamentalAnalysis",
    "SentimentAnalysis",
    "TokenData",
    "Verdict",
    "__version__",
]
