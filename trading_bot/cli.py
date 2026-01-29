#!/usr/bin/env python3
"""
Trading Bot CLI - Binance Futures Testnet
"""

import argparse
import os
import sys
from typing import Optional

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.orders import OrderManager
from trading_bot.bot.validators import validate_api_credentials, validate_quantity, validate_price

def get_api_credentials() -> tuple[str, str]:
    """Get API credentials from environment variables."""
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ Error: API credentials not found!")
        print("Please set the following environment variables:")
        print("  BINANCE_API_KEY=your_api_key")
        print("  BINANCE_API_SECRET=your_api_secret")
        sys.exit(1)
    
    if not validate_api_credentials(api_key, api_secret):
        print("❌ Error: Invalid API credentials format!")
        sys.exit(1)
    
    return api_key, api_secret

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description='Trading Bot for Binance Futures Testnet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Market buy order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  # Limit sell order
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500.50

  # Check account info
  python cli.py --account-info
        """
    )
    
    parser.add_argument('--symbol', type=str, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--type', choices=['MARKET', 'LIMIT'], help='Order type')
    parser.add_argument('--quantity', type=str, help='Order quantity')
    parser.add_argument('--price', type=str, help='Order price (required for LIMIT orders)')
    parser.add_argument('--account-info', action='store_true', help='Show account information')
    
    return parser

def validate_args(args) -> bool:
    """Validate command line arguments."""
    if args.account_info:
        return True
    
    # Check required arguments for order placement
    if not all([args.symbol, args.side, args.type, args.quantity]):
        print("❌ Error: Missing required arguments for order placement!")
        print("Required: --symbol, --side, --type, --quantity")
        return False
    
    # Validate quantity
    quantity = validate_quantity(args.quantity)
    if quantity is None:
        print(f"❌ Error: Invalid quantity '{args.quantity}'. Must be a positive number.")
        return False
    
    # Validate price for LIMIT orders
    if args.type == 'LIMIT':
        if not args.price:
            print("❌ Error: --price is required for LIMIT orders!")
            return False
        
        price = validate_price(args.price)
        if price is None:
            print(f"❌ Error: Invalid price '{args.price}'. Must be a positive number.")
            return False
    
    return True

def main():
    """Main CLI entry point."""
    # Setup logging
    logger = setup_logging()
    logger.info("Trading Bot CLI started")
    
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate arguments
    if not validate_args(args):
        parser.print_help()
        sys.exit(1)
    
    try:
        # Get API credentials
        api_key, api_secret = get_api_credentials()
        
        # Initialize client and order manager
        client = BinanceFuturesClient(api_key, api_secret)
        order_manager = OrderManager(client)
        
        if args.account_info:
            # Show account information
            print("Fetching account information...")
            account_info = client.get_account_info()
            
            print("\n" + "="*50)
            print("ACCOUNT INFORMATION")
            print("="*50)
            print(f"Total Wallet Balance: {account_info.get('totalWalletBalance', 'N/A')} USDT")
            print(f"Available Balance: {account_info.get('availableBalance', 'N/A')} USDT")
            print(f"Total Unrealized PnL: {account_info.get('totalUnrealizedProfit', 'N/A')} USDT")
            print("="*50)
            
        else:
            # Place order
            quantity = validate_quantity(args.quantity)
            price = validate_price(args.price) if args.price else None
            
            # Print order summary
            order_manager.print_order_summary(args.symbol, args.side, args.type, quantity, price)
            
            # Confirm order placement
            confirm = input("\nDo you want to place this order? (y/N): ").strip().lower()
            if confirm != 'y':
                print("Order cancelled by user.")
                sys.exit(0)
            
            # Place the order
            print("\nPlacing order...")
            response = order_manager.place_order(args.symbol, args.side, args.type, quantity, price)
            
            # Print response
            order_manager.print_order_response(response)
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()