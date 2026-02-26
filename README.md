# MuppinLLM 🐂

<p align="center">
  <img src="https://muppin.fun/wp-content/uploads/2026/02/ezgif.com-gif-maker.gif" alt="Muppin The Bull" width="200">
</p>

<p align="center">
  <strong>AI-Powered Crypto Market Analyst for Solana Tokens</strong>
</p>

<p align="center">
  <a href="https://muppin.fun">Website</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#api-reference">API Reference</a>
</p>

---

## The Mind of The Bull

**Muppin isn't just a mascot—he is an autonomous AI agent engineered to embody the relentless energy of a bull market.**

MuppinLLM analyzes Solana tokens using:
- 📊 **Technical Analysis**: RSI, MACD, Bollinger Bands, Moving Averages
- 💎 **Fundamental Analysis**: Liquidity, Volume, Token Age, DEX Presence
- 🎭 **Sentiment Analysis**: Social Media, Community Activity, Market Vibes
- 🤖 **AI-Powered Insights**: OpenAI GPT-4o powered market analysis

Get a clear **BULLISH** or **BEARISH** verdict with confidence scores!

## Installation

```bash
pip install git+https://github.com/muppinai/muppinllm.git
```

Or install from source:

```bash
git clone https://github.com/muppinai/muppinllm.git
cd muppinllm
pip install -e .
```

## Quick Start

### Python API

```python
import asyncio
from muppinllm import MuppinAnalyst

async def main():
    # Initialize the analyst with your OpenAI API key
    analyst = MuppinAnalyst(api_key="your-openai-api-key")
    
    # Analyze a Solana token by contract address
    result = await analyst.analyze("JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN")
    
    # Get the verdict
    print(f"Token: {result.token.symbol}")
    print(f"Verdict: {result.verdict}")  # BULLISH, BEARISH, NEUTRAL, etc.
    print(f"Strength: {result.strength}/100")
    print(f"Combined Score: {result.combined_score}/100")
    
    # Detailed analysis
    print(f"\nTechnical Score: {result.technical.score}/100")
    print(f"Fundamental Score: {result.fundamental.score}/100")
    print(f"Sentiment Score: {result.sentiment.sentiment_score}/100")
    
    # AI Summary
    print(f"\nAI Analysis: {result.ai_summary}")
    print(f"Recommendation: {result.ai_recommendation}")
    
    await analyst.close()

asyncio.run(main())
```

### Command Line Interface

```bash
# Set your API key
export OPENAI_API_KEY="sk-your-openai-api-key"

# Analyze a token
muppinllm analyze JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN

# Get JSON output
muppinllm analyze JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN --json

# Fast analysis without AI (just numerical analysis)
muppinllm analyze JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN --no-ai

# Use a different model
muppinllm analyze JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN --model gpt-4-turbo

# Get Solana market sentiment
muppinllm market

# Search for tokens
muppinllm search jupiter
```

## Features

### Verdicts

MuppinLLM provides clear market verdicts:

| Verdict | Score Range | Description |
|---------|-------------|-------------|
| EXTREMELY_BULLISH | 80-100 | Strong buy signals across all metrics |
| BULLISH | 65-79 | Positive outlook with good fundamentals |
| SLIGHTLY_BULLISH | 55-64 | Leaning positive, watch for confirmation |
| NEUTRAL | 46-54 | Mixed signals, wait for clarity |
| SLIGHTLY_BEARISH | 36-45 | Leaning negative, be cautious |
| BEARISH | 21-35 | Negative outlook, consider exits |
| EXTREMELY_BEARISH | 0-20 | Strong sell signals, high risk |

### Technical Indicators

- **RSI (14)**: Relative Strength Index for overbought/oversold conditions
- **MACD**: Moving Average Convergence Divergence for momentum
- **Bollinger Bands**: Volatility and price position analysis
- **Moving Averages**: SMA-20, SMA-50, EMA-12, EMA-26
- **Volume Analysis**: Volume trends and anomalies
- **Support/Resistance**: Key price levels

### Fundamental Metrics

- **Liquidity Analysis**: Pool liquidity rating (excellent to very_low)
- **Volume Analysis**: 24h trading volume assessment
- **Token Age**: Maturity rating (new, young, established, mature)
- **DEX Presence**: Number of pools and DEX listings
- **Market Cap & FDV**: Valuation metrics

### Sentiment Analysis

- **Price Momentum**: Recent price action sentiment
- **Transaction Analysis**: Buy/sell ratio
- **Community Activity**: Social media presence
- **Overall Sentiment**: POSITIVE, NEGATIVE, NEUTRAL, MIXED

## API Reference

### MuppinAnalyst

```python
class MuppinAnalyst:
    def __init__(
        self,
        api_key: str,                    # OpenAI API key
        model: str = "gpt-4o",           # OpenAI model (gpt-4o, gpt-4-turbo, gpt-3.5-turbo)
        coingecko_api_key: str = None    # Optional CoinGecko Pro key
    )
    
    async def analyze(
        self,
        contract_address: str,           # Solana token address
        include_ai_analysis: bool = True # Include AI-powered analysis
    ) -> AnalysisResult
    
    async def analyze_multiple(
        self,
        contract_addresses: List[str],
        include_ai_analysis: bool = False
    ) -> List[AnalysisResult]
    
    async def get_market_sentiment(self) -> Dict[str, Any]
```

### AnalysisResult

```python
@dataclass
class AnalysisResult:
    token: TokenData                    # Token information
    technical: TechnicalAnalysis        # Technical analysis results
    fundamental: FundamentalAnalysis    # Fundamental analysis results
    sentiment: SentimentAnalysis        # Sentiment analysis results
    
    verdict: Verdict                    # Final verdict (BULLISH/BEARISH/etc)
    strength: int                       # Confidence strength (1-100)
    combined_score: float               # Overall score (0-100)
    
    ai_summary: str                     # AI-generated summary
    ai_recommendation: str              # AI recommendation
    risk_factors: List[str]             # Identified risks
    opportunities: List[str]            # Identified opportunities
    
    def to_dict(self) -> Dict[str, Any]  # Convert to dictionary
```

## Data Sources

MuppinLLM aggregates data from multiple sources:

- **DexScreener**: Real-time DEX data, pools, prices, volumes
- **CoinGecko**: Token metadata, community data, additional metrics

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI analysis | Yes (for AI features) |
| `COINGECKO_API_KEY` | CoinGecko Pro API key | No |

## Getting an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Set it as environment variable: `export OPENAI_API_KEY="sk-your-key"`

## Examples

### Analyze Multiple Tokens

```python
async def analyze_portfolio():
    analyst = MuppinAnalyst(api_key="your-key")
    
    tokens = [
        "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",  # JUP
        "So11111111111111111111111111111111111111112",   # SOL
        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", # USDC
    ]
    
    results = await analyst.analyze_multiple(tokens)
    
    for result in results:
        print(f"{result.token.symbol}: {result.verdict} ({result.strength}%)")
    
    await analyst.close()
```

### Custom Weighting

```python
result = await analyst.analyze("token-address")

# Customize weights for final score
custom_score = (
    result.technical.score * 0.5 +      # More weight on technical
    result.fundamental.score * 0.3 +     # Less on fundamental
    result.sentiment.sentiment_score * 0.2  # Least on sentiment
)
```

### Export to JSON

```python
result = await analyst.analyze("token-address")
data = result.to_dict()

import json
with open("analysis.json", "w") as f:
    json.dump(data, f, indent=2)
```

## Supported OpenAI Models

| Model | Description | Cost |
|-------|-------------|------|
| `gpt-4o` | Latest GPT-4o (default, recommended) | $$ |
| `gpt-4-turbo` | GPT-4 Turbo | $$ |
| `gpt-4` | GPT-4 | $$$ |
| `gpt-3.5-turbo` | GPT-3.5 (faster, cheaper) | $ |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file.

## Links

- 🌐 Website: [muppin.fun](https://muppin.fun)
- 📦 GitHub: [muppinai/muppinllm](https://github.com/muppinai/muppinllm)

---

<p align="center">
  <strong>Muppin - The Mind of The Bull</strong><br>
  <em>Powered by OpenAI. Fueled by the Stampede.</em>
</p>
