"""
CoinGecko API integration for fetching additional token data.
"""
import aiohttp
import asyncio
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class CoinGeckoAPI:
    """
    CoinGecko API client for fetching token metadata and market data.
    
    Note: Uses free API tier with rate limits (10-30 calls/minute).
    For production use, consider using Pro API.
    """
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        """
        Initialize CoinGecko API client.
        
        Args:
            api_key: Optional CoinGecko Pro API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            headers = {}
            if self.api_key:
                headers["x-cg-pro-api-key"] = self.api_key
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers=headers
            )
        return self._session
    
    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Make a GET request to CoinGecko API."""
        session = await self._get_session()
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    logger.warning("CoinGecko rate limit reached")
                    return None
                else:
                    logger.warning(f"CoinGecko API error: {response.status}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"CoinGecko API timeout for {url}")
            return None
        except Exception as e:
            logger.error(f"CoinGecko API error: {e}")
            return None
    
    async def get_token_by_contract(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """
        Get token data by contract address on Solana.
        
        Args:
            contract_address: Solana token contract address
            
        Returns:
            Token data dictionary or None
        """
        endpoint = f"/coins/solana/contract/{contract_address}"
        return await self._request(endpoint)
    
    async def get_token_market_chart(
        self,
        contract_address: str,
        days: int = 7,
        interval: str = "daily"
    ) -> Optional[Dict[str, Any]]:
        """
        Get historical market data for a token.
        
        Args:
            contract_address: Solana token contract address
            days: Number of days of data (1, 7, 14, 30, 90, 180, 365, max)
            interval: Data interval (daily, hourly for <90 days)
            
        Returns:
            Market chart data with prices, volumes, market_caps
        """
        endpoint = f"/coins/solana/contract/{contract_address}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
        }
        return await self._request(endpoint, params)
    
    async def get_token_info(self, contract_address: str) -> Optional[Dict[str, Any]]:
        """
        Get basic token info (name, symbol, description, links).
        
        Args:
            contract_address: Solana token contract address
            
        Returns:
            Token info dictionary
        """
        data = await self.get_token_by_contract(contract_address)
        
        if not data:
            return None
        
        return {
            "id": data.get("id"),
            "symbol": data.get("symbol"),
            "name": data.get("name"),
            "description": data.get("description", {}).get("en"),
            "image": data.get("image", {}),
            "links": data.get("links", {}),
            "categories": data.get("categories", []),
            "sentiment_votes_up_percentage": data.get("sentiment_votes_up_percentage"),
            "sentiment_votes_down_percentage": data.get("sentiment_votes_down_percentage"),
            "market_cap_rank": data.get("market_cap_rank"),
            "coingecko_rank": data.get("coingecko_rank"),
            "coingecko_score": data.get("coingecko_score"),
            "developer_score": data.get("developer_score"),
            "community_score": data.get("community_score"),
            "liquidity_score": data.get("liquidity_score"),
            "public_interest_score": data.get("public_interest_score"),
            "market_data": data.get("market_data", {}),
            "community_data": data.get("community_data", {}),
            "developer_data": data.get("developer_data", {}),
        }
    
    async def get_global_data(self) -> Optional[Dict[str, Any]]:
        """
        Get global cryptocurrency market data.
        
        Returns:
            Global market data including total market cap, volume, etc.
        """
        endpoint = "/global"
        return await self._request(endpoint)
    
    async def get_solana_price(self) -> Optional[float]:
        """
        Get current Solana (SOL) price in USD.
        
        Returns:
            SOL price in USD
        """
        endpoint = "/simple/price"
        params = {
            "ids": "solana",
            "vs_currencies": "usd"
        }
        data = await self._request(endpoint, params)
        
        if data and "solana" in data:
            return data["solana"].get("usd")
        return None
    
    async def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for tokens by name or symbol.
        
        Args:
            query: Search query
            
        Returns:
            List of matching coins
        """
        endpoint = "/search"
        params = {"query": query}
        data = await self._request(endpoint, params)
        
        if data and "coins" in data:
            return data["coins"]
        return []
    
    async def get_trending(self) -> List[Dict[str, Any]]:
        """
        Get trending coins on CoinGecko.
        
        Returns:
            List of trending coins
        """
        endpoint = "/search/trending"
        data = await self._request(endpoint)
        
        if data and "coins" in data:
            return [coin.get("item", {}) for coin in data["coins"]]
        return []
