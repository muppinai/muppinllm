"""
Helper utility functions for MuppinLLM.
"""
from typing import Optional, Union


def format_number(value: Optional[Union[int, float]], decimals: int = 2) -> str:
    """
    Format a number with appropriate suffix (K, M, B, T).
    
    Args:
        value: Number to format
        decimals: Decimal places
        
    Returns:
        Formatted string (e.g., "1.5M")
    """
    if value is None:
        return "N/A"
    
    if abs(value) >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.{decimals}f}T"
    elif abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.{decimals}f}B"
    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{decimals}f}M"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.{decimals}f}K"
    else:
        return f"{value:.{decimals}f}"


def format_percentage(value: Optional[float], decimals: int = 2) -> str:
    """
    Format a percentage value.
    
    Args:
        value: Percentage value
        decimals: Decimal places
        
    Returns:
        Formatted string (e.g., "+5.25%" or "-3.10%")
    """
    if value is None:
        return "N/A"
    
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.{decimals}f}%"


def format_usd(value: Optional[float], decimals: int = 2) -> str:
    """
    Format a USD value.
    
    Args:
        value: USD value
        decimals: Decimal places
        
    Returns:
        Formatted string (e.g., "$1.5M")
    """
    if value is None:
        return "N/A"
    
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.{decimals}f}B"
    elif abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.{decimals}f}M"
    elif abs(value) >= 1_000:
        return f"${value / 1_000:.{decimals}f}K"
    elif abs(value) >= 1:
        return f"${value:.{decimals}f}"
    else:
        # For very small values (crypto prices)
        return f"${value:.8f}"


def calculate_change_percentage(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100


def validate_solana_address(address: str) -> bool:
    """
    Validate a Solana address format.
    
    Args:
        address: Address string to validate
        
    Returns:
        True if valid format, False otherwise
    """
    # Solana addresses are base58 encoded, 32-44 characters
    if not address or not isinstance(address, str):
        return False
    
    if len(address) < 32 or len(address) > 44:
        return False
    
    # Base58 characters
    base58_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return all(c in base58_chars for c in address)
