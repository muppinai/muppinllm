"""
MuppinLLM Command Line Interface.

Usage:
    muppinllm analyze <contract_address>
    muppinllm market
"""
import asyncio
import argparse
import json
import sys
import os
from dotenv import load_dotenv


def main():
    """Main CLI entry point."""
    load_dotenv()
    
    parser = argparse.ArgumentParser(
        description="MuppinLLM - AI-Powered Crypto Market Analyst for Solana Tokens",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  muppinllm analyze So11111111111111111111111111111111111111112
  muppinllm analyze JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN --json
  muppinllm market

Environment Variables:
  EMERGENT_LLM_KEY    Your Emergent LLM API key
  COINGECKO_API_KEY   Optional CoinGecko Pro API key

For more info: https://muppin.fun
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a Solana token")
    analyze_parser.add_argument(
        "contract_address",
        help="Solana token contract address"
    )
    analyze_parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    analyze_parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Skip AI-powered analysis (faster)"
    )
    analyze_parser.add_argument(
        "--api-key",
        help="Emergent LLM API key (or set EMERGENT_LLM_KEY)"
    )
    
    # Market command
    market_parser = subparsers.add_parser("market", help="Get Solana market sentiment")
    market_parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for tokens")
    search_parser.add_argument(
        "query",
        help="Search query (name or symbol)"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Run async command
    asyncio.run(run_command(args))


async def run_command(args):
    """Run the appropriate command."""
    from .analyst import MuppinAnalyst
    
    api_key = getattr(args, "api_key", None) or os.environ.get("EMERGENT_LLM_KEY")
    
    if args.command == "analyze":
        if not api_key:
            print("Error: EMERGENT_LLM_KEY not set. Set environment variable or use --api-key")
            sys.exit(1)
        
        async with MuppinAnalyst(api_key=api_key) as analyst:
            try:
                result = await analyst.analyze(
                    args.contract_address,
                    include_ai_analysis=not args.no_ai
                )
                
                if args.json:
                    print(json.dumps(result.to_dict(), indent=2))
                else:
                    print(result)
                    print(f"\n{result.ai_summary}")
                    if result.ai_recommendation:
                        print(f"\nRecommendation: {result.ai_recommendation}")
                    if result.risk_factors:
                        print(f"\nRisk Factors:")
                        for risk in result.risk_factors:
                            print(f"  - {risk}")
                    if result.opportunities:
                        print(f"\nOpportunities:")
                        for opp in result.opportunities:
                            print(f"  - {opp}")
            
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
    
    elif args.command == "market":
        async with MuppinAnalyst(api_key=api_key or "dummy") as analyst:
            sentiment = await analyst.get_market_sentiment()
            
            if args.json:
                print(json.dumps(sentiment, indent=2))
            else:
                print("\n=== SOLANA MARKET SENTIMENT ===")
                print(f"SOL Price: ${sentiment.get('sol_price_usd', 'N/A')}")
                print(f"Trending Tokens: {sentiment.get('trending_tokens', 0)}")
                print(f"Timestamp: {sentiment.get('timestamp', 'N/A')}")
    
    elif args.command == "search":
        from .data_sources import DexScreenerAPI
        
        async with DexScreenerAPI() as dex:
            results = await dex.search_tokens(args.query)
            
            if not results:
                print("No tokens found")
                return
            
            print(f"\nFound {len(results)} tokens:\n")
            for pair in results[:10]:
                base = pair.get("baseToken", {})
                print(f"  {base.get('symbol', '???')} - {base.get('name', 'Unknown')}")
                print(f"    Contract: {base.get('address', 'N/A')}")
                print(f"    Price: ${pair.get('priceUsd', 'N/A')}")
                print()


if __name__ == "__main__":
    main()
