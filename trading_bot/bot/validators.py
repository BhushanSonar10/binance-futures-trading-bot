import re
from typing import Optional

def validate_symbol(symbol: str) -> bool:
    """Validate trading symbol format."""
    if not symbol:
        return False
    
    # Basic validation for crypto pairs (e.g., BTCUSDT)
    pattern = r'^[A-Z]{2,10}USDT$'
    return bool(re.match(pattern, symbol.upper()))

def validate_side(side: str) -> bool:
    """Validate order side."""
    return side.upper() in ['BUY', 'SELL']

def validate_order_type(order_type: str) -> bool:
    """Validate order type."""
    return order_type.upper() in ['MARKET', 'LIMIT']

def validate_quantity(quantity: str) -> Optional[float]:
    """Validate and convert quantity to float."""
    try:
        qty = float(quantity)
        if qty <= 0:
            return None
        return qty
    except (ValueError, TypeError):
        return None

def validate_price(price: str) -> Optional[float]:
    """Validate and convert price to float."""
    try:
        p = float(price)
        if p <= 0:
            return None
        return p
    except (ValueError, TypeError):
        return None

def validate_api_credentials(api_key: str, api_secret: str) -> bool:
    """Validate API credentials format."""
    if not api_key or not api_secret:
        return False
    
    # Basic length validation
    if len(api_key) < 10 or len(api_secret) < 10:
        return False
    
    return True