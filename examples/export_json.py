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
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    
    if not api_key:
        print("Error: Please set EMERGENT_LLM_KEY environment variable")
        return
    
    # Token to analyze
    token_address = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
    
    async with MuppinAnalyst(api_key=api_key) as analyst:
        print(f"Analyzing token: {token_address}")
        
        result = await analyst.analyze(token_address)
        
        # Convert to dictionary
        data = result.to_dict()
        
        # Add metadata
        data["metadata"] = {
            "analyzed_by": "MuppinLLM",
            "version": "1.0.0",
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
