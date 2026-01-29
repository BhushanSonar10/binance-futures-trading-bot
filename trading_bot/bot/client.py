import requests
import time
import hmac
import hashlib
import logging
from typing import Dict, Any, Optional
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    """Binance Futures Testnet API client."""
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com"
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        })
    
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """Generate HMAC SHA256 signature for API requests."""
        query_string = urlencode(params)
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None, signed: bool = False) -> Dict[str, Any]:
        """Make HTTP request to Binance API."""
        if params is None:
            params = {}
        
        url = f"{self.base_url}{endpoint}"
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        try:
            logger.info(f"Making {method} request to {endpoint} with params: {params}")
            
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"API Response: {result}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    logger.error(f"API Error Details: {error_data}")
                except:
                    logger.error(f"API Error Response: {e.response.text}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        return self._make_request('GET', '/fapi/v2/account', signed=True)
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get symbol information from exchange info."""
        exchange_info = self._make_request('GET', '/fapi/v1/exchangeInfo')
        
        for symbol_info in exchange_info.get('symbols', []):
            if symbol_info['symbol'] == symbol.upper():
                return symbol_info
        return None
    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
        """Place an order on Binance Futures."""
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': str(quantity)
        }
        
        if order_type.upper() == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params['price'] = str(price)
            params['timeInForce'] = 'GTC'  # Good Till Cancelled
        
        return self._make_request('POST', '/fapi/v1/order', params, signed=True)