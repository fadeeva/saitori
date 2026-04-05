# Saitori. Exchange Simulator

**A complete exchange simulation engine** implementing core trading system mechanisms.

## Core Systems
- **Matching Engine** - Price-time priority with partial fills
- **Order Logger** - Complete order lifecycle tracking
- **Trades Book** - All executed trades with audit trail
- **Market Depth** - Aggregated bid/ask levels for visualization

## Order Types
- **Limit orders** - Execute at specified price or better
- **Market orders** - Immediate execution at best available price
- **Stop orders** - Activate when market price reaches stop price
  - Stop Limit - Becomes limit order after activation
  - Stop Market - Becomes market order after activation

## Time-in-Force
- **GTC** (Good Till Cancelled) - Order lives until filled or cancelled
- **IOC** (Immediate or Cancel) - Execute available portion, cancel remainder
- **FOK** (Fill or Kill) - Execute fully or cancel entirely