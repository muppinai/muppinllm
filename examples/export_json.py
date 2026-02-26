"""
Example: Export Analysis to JSON

Analyze a token and export the results to a JSON file.
"""
import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from muppinllm import MuppinAnalyst


async def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Warning: OPENAI_API_KEY not set. Running without AI analysis.")
        api_key = "dummy"
    
    # Token to analyze
    token_address = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
    
    async with MuppinAnalyst(api_key=api_key) as analyst:
        print(f"Analyzing token: {token_address}")
        
        # Run without AI if no API key
        include_ai = api_key != "dummy"
        result = await analyst.analyze(token_address, include_ai_analysis=include_ai)
        
        # Convert to dictionary
        data = result.to_dict()
        
        # Add metadata
        data["metadata"] = {
            "analyzed_by": "MuppinLLM",
            "version": "1.0.1",
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Save to file
        filename = f"analysis_{result.token.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"\n✓ Analysis saved to: {filename}")
        print(f"\nQuick summary:")
        print(f"  Token: {result.token.symbol}")
        print(f"  Verdict: {result.verdict.value}")
        print(f"  Score: {result.combined_score}/100")


if __name__ == "__main__":
    asyncio.run(main())
