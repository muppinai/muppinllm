"""
Example: Portfolio Analysis

Analyze multiple tokens and compare their signals.
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from muppinllm import MuppinAnalyst


# Sample portfolio of popular Solana tokens
PORTFOLIO = {
    "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": "JUP (Jupiter)",
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": "BONK",
}


async def main():
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    
    if not api_key:
        print("Error: Please set EMERGENT_LLM_KEY environment variable")
        return
    
    async with MuppinAnalyst(api_key=api_key) as analyst:
        print("=" * 60)
        print("MUPPIN PORTFOLIO ANALYSIS")
        print("=" * 60)
        
        results = []
        
        for address, name in PORTFOLIO.items():
            print(f"\nAnalyzing {name}...")
            
            try:
                # Use no AI for faster bulk analysis
                result = await analyst.analyze(address, include_ai_analysis=False)
                results.append((name, result))
                
                print(f"  ✓ {result.verdict.value} (Score: {result.combined_score:.1f})")
            
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        # Summary table
        print("\n" + "=" * 60)
        print("PORTFOLIO SUMMARY")
        print("=" * 60)
        print(f"{'Token':<20} {'Verdict':<20} {'Score':<10} {'24h Change':<10}")
        print("-" * 60)
        
        for name, result in results:
            change = f"{result.token.price_change_24h:.2f}%" if result.token.price_change_24h else "N/A"
            print(f"{name:<20} {result.verdict.value:<20} {result.combined_score:<10.1f} {change:<10}")
        
        # Best and worst performers
        if results:
            sorted_results = sorted(results, key=lambda x: x[1].combined_score, reverse=True)
            
            print("\n" + "=" * 60)
            print(f"🥇 Best Signal: {sorted_results[0][0]} ({sorted_results[0][1].verdict.value})")
            print(f"🥉 Weakest Signal: {sorted_results[-1][0]} ({sorted_results[-1][1].verdict.value})")


if __name__ == "__main__":
    asyncio.run(main())
