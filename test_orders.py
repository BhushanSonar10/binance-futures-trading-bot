#!/usr/bin/env python3
"""
Test script to demonstrate trading bot functionality
This script will attempt to place test orders (requires valid API credentials)
"""

import os
import sys
from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.orders import OrderManager

def test_orders():
    """Test order placement functionality."""
    # Setup logging
    logger = setup_logging()
    logger.info("Starting test orders")
    
    # Get API credentials from environment
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables")
        return
    
    try:
        # Initialize client and order manager
        client = BinanceFuturesClient(api_key, api_secret)
        order_manager = OrderManager(client)
        
        print("Testing account connection...")
        account_info = client.get_account_info()
        print(f"✅ Connected! Available balance: {account_info.get('availableBalance', 'N/A')} USDT")
        
        # Test 1: Market Order
        print("\n" + "="*60)
        print("TEST 1: MARKET BUY ORDER")
        print("="*60)
        
        try:
            order_manager.print_order_summary("BTCUSDT", "BUY", "MARKET", 0.001)
            # Uncomment the line below to actually place the order
            # response = order_manager.place_order("BTCUSDT", "BUY", "MARKET", 0.001)
            # order_manager.print_order_response(response)
            print("📝 Market order test completed (order not actually placed)")
        except Exception as e:
            logger.error(f"Market order test failed: {e}")
            print(f"❌ Market order test failed: {e}")
        
        # Test 2: Limit Order
        print("\n" + "="*60)
        print("TEST 2: LIMIT SELL ORDER")
        print("="*60)
        
        try:
            order_manager.print_order_summary("ETHUSDT", "SELL", "LIMIT", 0.01, 2500.50)
            # Uncomment the line below to actually place the order
            # response = order_manager.place_order("ETHUSDT", "SELL", "LIMIT", 0.01, 2500.50)
            # order_manager.print_order_response(response)
            print("📝 Limit order test completed (order not actually placed)")
        except Exception as e:
            logger.error(f"Limit order test failed: {e}")
            print(f"❌ Limit order test failed: {e}")
        
        print("\n✅ All tests completed! Check the logs/ directory for detailed logs.")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"❌ Test failed: {e}")

if __name__ == '__main__':
    test_orders()