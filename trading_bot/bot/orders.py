import logging
from typing import Dict, Any, Optional
from .client import BinanceFuturesClient
from .validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price

logger = logging.getLogger(__name__)

class OrderManager:
    """Handles order placement and management."""
    
    def __init__(self, client: BinanceFuturesClient):
        self.client = client
    
    def validate_order_params(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> bool:
        """Validate order parameters."""
        if not validate_symbol(symbol):
            logger.error(f"Invalid symbol: {symbol}")
            return False
        
        if not validate_side(side):
            logger.error(f"Invalid side: {side}. Must be BUY or SELL")
            return False
        
        if not validate_order_type(order_type):
            logger.error(f"Invalid order type: {order_type}. Must be MARKET or LIMIT")
            return False
        
        if quantity <= 0:
            logger.error(f"Invalid quantity: {quantity}. Must be positive")
            return False
        
        if order_type.upper() == 'LIMIT' and (price is None or price <= 0):
            logger.error(f"Invalid price for LIMIT order: {price}. Must be positive")
            return False
        
        return True
    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
        """Place an order with validation."""
        logger.info(f"Attempting to place {order_type} {side} order for {quantity} {symbol}")
        
        # Validate parameters
        if not self.validate_order_params(symbol, side, order_type, quantity, price):
            raise ValueError("Invalid order parameters")
        
        # Check symbol exists on exchange
        symbol_info = self.client.get_symbol_info(symbol)
        if not symbol_info:
            raise ValueError(f"Symbol {symbol} not found on exchange")
        
        logger.info(f"Symbol {symbol} validated successfully")
        
        # Place the order
        try:
            result = self.client.place_order(symbol, side, order_type, quantity, price)
            logger.info(f"Order placed successfully: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            raise
    
    def print_order_summary(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None):
        """Print order request summary."""
        print("\n" + "="*50)
        print("ORDER REQUEST SUMMARY")
        print("="*50)
        print(f"Symbol: {symbol.upper()}")
        print(f"Side: {side.upper()}")
        print(f"Type: {order_type.upper()}")
        print(f"Quantity: {quantity}")
        if price is not None:
            print(f"Price: {price}")
        print("="*50)
    
    def print_order_response(self, response: Dict[str, Any]):
        """Print order response details."""
        print("\nORDER RESPONSE DETAILS")
        print("="*50)
        print(f"Order ID: {response.get('orderId', 'N/A')}")
        print(f"Status: {response.get('status', 'N/A')}")
        print(f"Executed Quantity: {response.get('executedQty', 'N/A')}")
        
        if 'avgPrice' in response and response['avgPrice'] != '0':
            print(f"Average Price: {response['avgPrice']}")
        
        print(f"Client Order ID: {response.get('clientOrderId', 'N/A')}")
        print(f"Update Time: {response.get('updateTime', 'N/A')}")
        print("="*50)
        
        # Success message
        if response.get('status') in ['FILLED', 'NEW', 'PARTIALLY_FILLED']:
            print("✅ ORDER PLACED SUCCESSFULLY!")
        else:
            print("⚠️  ORDER STATUS UNCLEAR - CHECK LOGS")