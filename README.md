# Trading Bot - Binance Futures Testnet

A Python trading bot for placing orders on Binance Futures Testnet (USDT-M) with proper logging, error handling, and CLI interface.

## Features

- ✅ Place Market and Limit orders on Binance Futures Testnet
- ✅ Place Stop-Limit orders (STOP_MARKET and STOP) 
- ✅ Support for both BUY and SELL sides
- ✅ CLI interface with argument validation
- ✅ Comprehensive logging to files
- ✅ Structured, reusable code architecture
- ✅ Proper error handling and input validation
- ✅ Account information display

## Setup

### 1. Prerequisites

- Python 3.7+
- Binance Futures Testnet account
- API credentials from Binance Futures Testnet

### 2. Get Binance Futures Testnet API Credentials

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Register/Login to your account
3. Generate API Key and Secret Key
4. Note down your credentials (keep them secure!)

### 3. Installation

```bash
# Clone the repository
git clone https://github.com/BhushanSonar10/binance-futures-trading-bot.git
cd binance-futures-trading-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables (replace with your actual credentials)
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"

# On Windows (Command Prompt)
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here

# On Windows (PowerShell)
$env:BINANCE_API_KEY="your_api_key_here"
$env:BINANCE_API_SECRET="your_api_secret_here"
```

## Usage

### Command Line Interface

```bash
# Show help
python trading_bot/cli.py --help

# Check account information
python trading_bot/cli.py --account-info

# Place a Market BUY order
python trading_bot/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Place a Limit SELL order
python trading_bot/cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500.50

# Place a Stop Market order (stop loss)
python trading_bot/cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 45000

# Place a Stop Limit order (stop loss with limit price)
python trading_bot/cli.py --symbol BTCUSDT --side SELL --type STOP --quantity 0.001 --price 44500 --stop-price 45000
```

### Demo Mode (No API Required)

```bash
# Run demo to see bot functionality without API credentials
python demo.py
```

### Examples

#### Market Order Example
```bash
python trading_bot/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

#### Limit Order Example
```bash
python trading_bot/cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500.50
```

#### Stop-Limit Order Examples (Bonus Feature)
```bash
# Stop Market order (executes at market price when stop price is hit)
python trading_bot/cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 45000

# Stop Limit order (places limit order when stop price is hit)
python trading_bot/cli.py --symbol BTCUSDT --side SELL --type STOP --quantity 0.001 --price 44500 --stop-price 45000
```

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation functions
│   └── logging_config.py  # Logging configuration
├── cli.py                 # CLI entry point
├── __init__.py
├── README.md
├── requirements.txt
└── logs/                  # Log files (created automatically)
```

## Logging

All API requests, responses, and errors are logged to files in the `logs/` directory. Log files are named with timestamps for easy tracking:

- `logs/trading_bot_YYYYMMDD_HHMMSS.log`

## Error Handling

The bot includes comprehensive error handling for:

- Invalid API credentials
- Network failures
- Invalid input parameters
- API errors from Binance
- Missing required parameters

## Validation

Input validation includes:

- Symbol format validation (e.g., BTCUSDT)
- Order side validation (BUY/SELL)
- Order type validation (MARKET/LIMIT/STOP_MARKET/STOP)
- Quantity validation (positive numbers)
- Price validation (positive numbers, required for LIMIT and STOP orders)
- Stop price validation (positive numbers, required for STOP_MARKET and STOP orders)

## API Endpoints Used

- `GET /fapi/v1/exchangeInfo` - Get exchange information
- `GET /fapi/v2/account` - Get account information
- `POST /fapi/v1/order` - Place new order

## Assumptions

1. Using Binance Futures Testnet base URL: `https://testnet.binancefuture.com`
2. All orders are placed with `timeInForce=GTC` for LIMIT orders
3. API credentials are provided via environment variables for security
4. Using USDT-M futures (USDT-margined)
5. Minimum order quantities and price precision follow exchange rules

## Security Notes

- Never commit API credentials to version control
- Use environment variables for sensitive data
- API credentials are only for testnet (not real trading)
- All requests are signed with HMAC SHA256

## Testing

The bot has been tested with:
- Market orders (BUY/SELL)
- Limit orders (BUY/SELL)
- Stop-Limit orders (STOP_MARKET/STOP)
- Invalid input handling
- API error scenarios
- Network failure scenarios

## Troubleshooting

### Common Issues

1. **"API credentials not found"**
   - Ensure environment variables are set correctly
   - Check variable names: `BINANCE_API_KEY` and `BINANCE_API_SECRET`

2. **"Invalid symbol"**
   - Use correct symbol format (e.g., BTCUSDT, ETHUSDT)
   - Ensure symbol exists on Binance Futures

3. **"Insufficient balance"**
   - Check your testnet account balance
   - Request testnet funds from Binance Futures Testnet

4. **"Price precision error"**
   - Check the symbol's price precision requirements
   - Use appropriate decimal places for the trading pair

## License

This project is for educational and testing purposes only.
