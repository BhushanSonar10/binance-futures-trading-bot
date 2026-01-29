# Trading Bot Examples

This document provides detailed examples of how to use the trading bot.

## Prerequisites

Make sure you have:
1. Set up your API credentials as environment variables
2. Installed the required dependencies: `pip install -r requirements.txt`

## Basic Examples

### 1. Check Account Information

```bash
python cli.py --account-info
```

This will display your testnet account balance and other account details.

### 2. Market Orders

#### Market Buy Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

#### Market Sell Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### 3. Limit Orders

#### Limit Buy Order
```bash
python cli.py --symbol ETHUSDT --side BUY --type LIMIT --quantity 0.01 --price 2000.00
```

#### Limit Sell Order
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500.00
```

## Advanced Examples

### Different Trading Pairs

```bash
# BNB/USDT
python cli.py --symbol BNBUSDT --side BUY --type MARKET --quantity 0.1

# ADA/USDT
python cli.py --symbol ADAUSDT --side BUY --type LIMIT --quantity 10 --price 0.50

# DOT/USDT
python cli.py --symbol DOTUSDT --side SELL --type LIMIT --quantity 1 --price 15.00
```

### Precision Examples

Different symbols have different precision requirements:

```bash
# Bitcoin (high price, small quantities)
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 45000.50

# Ethereum (medium price, small quantities)
python cli.py --symbol ETHUSDT --side BUY --type LIMIT --quantity 0.01 --price 2500.75

# Lower priced coins (larger quantities)
python cli.py --symbol ADAUSDT --side BUY --type LIMIT --quantity 100 --price 0.45
```

## Error Handling Examples

The bot will handle various error scenarios:

### Invalid Symbol
```bash
python cli.py --symbol INVALIDPAIR --side BUY --type MARKET --quantity 0.001
# Output: ❌ Error: Invalid symbol: INVALIDPAIR
```

### Missing Price for Limit Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001
# Output: ❌ Error: --price is required for LIMIT orders!
```

### Invalid Quantity
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity -0.001
# Output: ❌ Error: Invalid quantity '-0.001'. Must be a positive number.
```

## Sample Output

### Successful Market Order
```
==================================================
ORDER REQUEST SUMMARY
==================================================
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.001
==================================================

Do you want to place this order? (y/N): y

Placing order...

ORDER RESPONSE DETAILS
==================================================
Order ID: 123456789
Status: FILLED
Executed Quantity: 0.001
Average Price: 45123.50
Client Order ID: abc123def456
Update Time: 1640995200000
==================================================
✅ ORDER PLACED SUCCESSFULLY!
```

### Successful Limit Order
```
==================================================
ORDER REQUEST SUMMARY
==================================================
Symbol: ETHUSDT
Side: SELL
Type: LIMIT
Quantity: 0.01
Price: 2500.0
==================================================

Do you want to place this order? (y/N): y

Placing order...

ORDER RESPONSE DETAILS
==================================================
Order ID: 987654321
Status: NEW
Executed Quantity: 0.000
Client Order ID: xyz789abc123
Update Time: 1640995200000
==================================================
✅ ORDER PLACED SUCCESSFULLY!
```

## Log Files

After running orders, check the `logs/` directory for detailed logs:

```
logs/
└── trading_bot_20240129_143022.log
```

The log files contain:
- API request details
- API response details
- Error messages and stack traces
- Validation results
- Timestamps for all operations

## Tips

1. **Start Small**: Use small quantities when testing
2. **Check Balance**: Always run `--account-info` first to check your testnet balance
3. **Monitor Logs**: Check log files for detailed information about API calls
4. **Price Precision**: Be aware of price precision requirements for different symbols
5. **Testnet Funds**: If you need more testnet funds, visit the Binance Futures Testnet website