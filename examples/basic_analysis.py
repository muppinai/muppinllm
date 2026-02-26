"""
Example: Basic Token Analysis

This example shows how to analyze a single Solana token
using MuppinLLM and interpret the results.
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from muppinllm import MuppinAnalyst


async def main():
    # Initialize the analyst with your API key
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    
    if not api_key:
        print("Error: Please set EMERGENT_LLM_KEY environment variable")
        print("Example: export EMERGENT_LLM_KEY=your-api-key")
        return
    
    async with MuppinAnalyst(api_key=api_key) as analyst:
        # Analyze Jupiter (JUP) token
        print("Analyzing Jupiter (JUP) token...\n")
        
        result = await analyst.analyze(
            "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
        )
        
        # Print the formatted report
        print(result)
        
        # Access individual components
        print("\n=== DETAILED BREAKDOWN ===\n")
        
        print(f"Token: {result.token.name} ({result.token.symbol})")
        print(f"Price: ${result.token.price_usd:.8f}")
        print(f"24h Change: {result.token.price_change_24h:.2f}%")
        print(f"Liquidity: ${result.token.liquidity_usd:,.0f}")
        
        print(f"\nTECHNICAL ANALYSIS:")
        print(f"  Score: {result.technical.score}/100 ({result.technical.signal})")
        print(f"  RSI(14): {result.technical.rsi_14} ({result.technical.rsi_signal})")
        print(f"  MACD: {result.technical.macd_trend}")
        print(f"  Trend: {result.technical.trend_direction}")
        
        print(f"\nFUNDAMENTAL ANALYSIS:")
        print(f"  Score: {result.fundamental.score}/100 ({result.fundamental.signal})")
        print(f"  Liquidity: {result.fundamental.liquidity_rating}")
        print(f"  Volume: {result.fundamental.volume_rating}")
        print(f"  Maturity: {result.fundamental.maturity_rating}")
        
        print(f"\nSENTIMENT ANALYSIS:")
        print(f"  Score: {result.sentiment.sentiment_score}/100 ({result.sentiment.signal})")
        print(f"  Overall: {result.sentiment.overall_sentiment}")
        print(f"  Community: {result.sentiment.community_activity}")
        
        print(f"\n=== AI ANALYSIS ===\n")
        print(f"Summary: {result.ai_summary}")
        print(f"\nRecommendation: {result.ai_recommendation}")
        
        if result.risk_factors:
            print(f"\nRisk Factors:")
            for risk in result.risk_factors:
                print(f"  - {risk}")
        
        if result.opportunities:
            print(f"\nOpportunities:")
            for opp in result.opportunities:
                print(f"  - {opp}")
        
        print(f"\n=== FINAL VERDICT ===")
        print(f"{'🐂' if 'BULLISH' in result.verdict.value else '🐻'} {result.verdict.value}")
        print(f"Strength: {result.strength}/100")


if __name__ == "__main__":
    asyncio.run(main())
