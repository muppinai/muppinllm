"""
DexScreener API integration for fetching Solana token data.
"""
import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DexScreenerAPI:
    """
    DexScreener API client for fetching Solana DEX data.
    
    Provides access to:
    - Token pairs and pools
    - Price data (current and historical)
    - Volume and liquidity metrics
    - DEX information
    """
    
    BASE_URL = "https://api.dexscreener.com"
    
    def __init__(self, timeout: int = 30):
        """
        Initialize DexScreener API client.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session
    
    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make a GET request to DexScreener API."""
        session = await self._get_session()
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"DexScreener API error: {response.status} for {url}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"DexScreener API timeout for {url}")
            return None
        except Exception as e:
            logger.error(f"DexScreener API error: {e}")
            return None
    
    async def get_token_pairs(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """
        Get all pairs/pools for a Solana token.
        
        Args:
            contract_address: Solana token contract address
            
        Returns:
            Dict containing pairs data or None if not found
        """
        endpoint = f"/token-pairs/v1/solana/{contract_address}"
        return await self._request(endpoint)
    
    async def get_token_data(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive token data from DexScreener.
        
        Args:
            contract_address: Solana token contract address
            
        Returns:
            Processed token data dictionary
        """
        data = await self.get_token_pairs(contract_address)
        
        if not data or not isinstance(data, list) or len(data) == 0:
            # Try alternative endpoint
            alt_endpoint = f"/latest/dex/tokens/{contract_address}"
            alt_data = await self._request(alt_endpoint)
            if alt_data and "pairs" in alt_data:
                data = alt_data["pairs"]
            else:
                return None
        
        # Find the pair with highest liquidity
        best_pair = None
        max_liquidity = 0
        
        pairs_list = data if isinstance(data, list) else data.get("pairs", [])
        
        for pair in pairs_list:
            liquidity = pair.get("liquidity", {}).get("usd", 0) or 0
            if liquidity > max_liquidity:
                max_liquidity = liquidity
                best_pair = pair
        
        if not best_pair:
            best_pair = pairs_list[0] if pairs_list else None
        
        if not best_pair:
            return None
        
        # Extract relevant data
        result = {
            "contract_address": contract_address,
            "name": best_pair.get("baseToken", {}).get("name"),
            "symbol": best_pair.get("baseToken", {}).get("symbol"),
            "price_usd": float(best_pair.get("priceUsd", 0) or 0),
            "price_native": float(best_pair.get("priceNative", 0) or 0),
            "price_change_24h": best_pair.get("priceChange", {}).get("h24"),
            "price_change_6h": best_pair.get("priceChange", {}).get("h6"),
            "price_change_1h": best_pair.get("priceChange", {}).get("h1"),
            "price_change_5m": best_pair.get("priceChange", {}).get("m5"),
            "volume_24h": best_pair.get("volume", {}).get("h24"),
            "volume_6h": best_pair.get("volume", {}).get("h6"),
            "volume_1h": best_pair.get("volume", {}).get("h1"),
            "liquidity_usd": best_pair.get("liquidity", {}).get("usd"),
            "fdv": best_pair.get("fdv"),
            "market_cap": best_pair.get("marketCap"),
            "pair_address": best_pair.get("pairAddress"),
            "dex_name": best_pair.get("dexId"),
            "pair_created_at": best_pair.get("pairCreatedAt"),
            "base_token": best_pair.get("baseToken", {}),
            "quote_token": best_pair.get("quoteToken", {}),
            "txns": best_pair.get("txns", {}),
            "info": best_pair.get("info", {}),
            "all_pairs": pairs_list,
        }
        
        # Extract social links from info
        info = best_pair.get("info", {})
        if info:
            result["website"] = info.get("websites", [{}])[0].get("url") if info.get("websites") else None
            socials = info.get("socials", [])
            for social in socials:
                if social.get("type") == "twitter":
                    result["twitter"] = social.get("url")
                elif social.get("type") == "telegram":
                    result["telegram"] = social.get("url")
                elif social.get("type") == "discord":
                    result["discord"] = social.get("url")
        
        return result
    
    async def get_multiple_tokens(self, addresses: List[str]) -> List[Dict[str, Any]]:
        """
        Get data for multiple tokens (max 30 at once).
        
        Args:
            addresses: List of Solana token contract addresses
            
        Returns:
            List of token data dictionaries
        """
        # DexScreener allows up to 30 addresses comma-separated
        addresses = addresses[:30]
        addresses_str = ",".join(addresses)
        
        endpoint = f"/token-pairs/v1/solana/{addresses_str}"
        data = await self._request(endpoint)
        
        if not data:
            return []
        
        return data if isinstance(data, list) else []
    
    async def search_tokens(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for tokens by name or symbol.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching tokens
        """
        endpoint = f"/latest/dex/search?q={query}"
        data = await self._request(endpoint)
        
        if not data or "pairs" not in data:
            return []
        
        # Filter for Solana tokens only
        solana_pairs = [
            pair for pair in data["pairs"]
            if pair.get("chainId") == "solana"
        ]
        
        return solana_pairs
    
    async def get_trending_tokens(self) -> List[Dict[str, Any]]:
        """
        Get trending Solana tokens.
        
        Returns:
            List of trending token pairs
        """
        endpoint = "/token-boosts/top/v1"
        data = await self._request(endpoint)
        
        if not data:
            return []
        
        # Filter for Solana
        return [
            token for token in data
            if token.get("chainId") == "solana"
        ]
