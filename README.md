# Binance Futures Testnet Trading Bot

A simplified, robust Python trading bot designed to place `MARKET` and `LIMIT` orders on the **Binance Futures Testnet** (USDT-M) avoiding complex wrapper libraries in favor of a direct REST mapping architecture.

## 🔗 Testnet URL
This application exclusively interfaces with the testnet base URL:
`https://testnet.binancefuture.com`

---

## 🛠 Project Structure
The project cleanly separates concerns into two layers per the requirements:
*   **CLI Layer**: `cli.py` (Command-line entry point using standard `argparse`).
*   **Client/API & Logic Layer**: Modularized in the `bot/` directory.

```text
trading_bot/
 ├── bot/
 │   ├── __init__.py
 │   ├── client.py        # Direct REST API client (HMAC SHA256 signing)
 │   ├── orders.py        # Payload formatting for orders
 │   ├── validators.py    # Input validation (symbol formats, pricing, bounds)
 │   └── logging_config.py# Centralized, file-based logging config
 |
 ├── cli.py               # argparse CLI implementation with explicit try/except
 |
 ├── README.md            
 └── requirements.txt     
```

---

## ⚙️ Setup Instructions

**1. Create & Activate a Virtual Environment**
```bash
python -m venv venv
# On Windows:
source venv/Scripts/activate
# On Mac/Linux:
source venv/bin/activate
```

**2. Install Requirements**
Included are lightweight, necessary requirements (`requests`, `python-dotenv`, `rich` for CLI aesthetics).
```bash
pip install -r requirements.txt
```

**3. Set Environment Variables**
A `.env` file must be created in the root directory containing your testnet keys.
```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

---

## 🚀 How to Run Examples

Using `argparse`, the CLI enforces named arguments for all inputs.

**1. Place a MARKET BUY Order**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**2. Place a LIMIT SELL Order (Requires Price)**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 65000
```

**3. View Help Instructions**
```bash
python cli.py --help
```

---

## 📋 Error Handling & Logging

### Error Handling Radar 🚨
Explicit `try-except` blocks have been built-in (both in `cli.py` and `bot/client.py`) intercepting `requests.exceptions.HTTPError`. These surface back to the UI seamlessly as a custom `BinanceAPIException`.
This safely handles:
*   `Invalid Symbol` API responses
*   `Insufficient Margin` errors
*   Network connection failures and timeouts
*   Wrong price for LIMIT (handled by pre-flight validation in `validators.py`).

### Logging
Logging is automatically piped to a static log file mapping:
`logs/trading.log`

The logs capture:
*   Request Payloads / Endpoints
*   Response Statuses and Response Data
*   Detailed API tracebacks when errors occur

---

## 💡 Assumptions Made
*   **Time-in-Force Binding:** Because `LIMIT` orders on the testnet explicitly require a `timeInForce` parameter, the bot automatically assumes and assigns `GTC` (Good-Till-Cancel) to limit orders to streamline CLI usage.
*   **Decoupled Library:** Relies on direct REST interactions using standard HTTP `requests` over the `python-binance` module to demonstrate core competency in exchange API mechanics (secure signature calculation, timestamp management).
