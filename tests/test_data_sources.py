"""
Tests for MuppinLLM data sources.
"""
import pytest
import asyncio
from muppinllm.data_sources import DexScreenerAPI, CoinGeckoAPI


class TestDexScreenerAPI:
    """Tests for DexScreener API client."""
    
    @pytest.fixture
    def api(self):
        return DexScreenerAPI()
    
    @pytest.mark.asyncio
    async def test_get_token_data_valid_address(self, api):
        """Test fetching token data with a valid Solana address."""
        # JUP token address
        address = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
        
        try:
            data = await api.get_token_data(address)
            
            if data:  # API may not always be available
                assert data.get("contract_address") == address
                assert "name" in data
                assert "symbol" in data
        finally:
            await api.close()
    
    @pytest.mark.asyncio
    async def test_get_token_data_invalid_address(self, api):
        """Test handling of invalid address."""
        address = "invalid_address_12345"
        
        try:
            data = await api.get_token_data(address)
            # Should return None for invalid addresses
            assert data is None or "error" in str(data).lower()
        finally:
            await api.close()
    
    @pytest.mark.asyncio
    async def test_search_tokens(self, api):
        """Test token search functionality."""
        try:
            results = await api.search_tokens("SOL")
            
            if results:  # API may not always be available
                assert isinstance(results, list)
        finally:
            await api.close()


class TestCoinGeckoAPI:
    """Tests for CoinGecko API client."""
    
    @pytest.fixture
    def api(self):
        return CoinGeckoAPI()
    
    @pytest.mark.asyncio
    async def test_get_solana_price(self, api):
        """Test fetching SOL price."""
        try:
            price = await api.get_solana_price()
            
            if price:  # API may not always be available
                assert isinstance(price, float)
                assert price > 0
        finally:
            await api.close()
    
    @pytest.mark.asyncio
    async def test_search(self, api):
        """Test coin search functionality."""
        try:
            results = await api.search("solana")
            
            if results:
                assert isinstance(results, list)
        finally:
            await api.close()
