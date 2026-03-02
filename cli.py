import argparse
import sys
import os
from dotenv import load_dotenv

# Optional rich imports for pretty output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    has_rich = True
except ImportError:
    has_rich = False

from bot.client import BinanceFuturesClient, BinanceAPIException
from bot.orders import place_order
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.logging_config import logger

# Load environment variables
load_dotenv()

def print_error(msg):
    if has_rich:
        console = Console()
        console.print(f"[bold red]ERROR:[/bold red] {msg}")
    else:
        print(f"ERROR: {msg}")

def print_success(msg):
    if has_rich:
        console = Console()
        console.print(f"[bold green]SUCCESS:[/bold green] {msg}")
    else:
        print(f"SUCCESS: {msg}")

def print_table(title, data):
    if has_rich:
        console = Console()
        table = Table(title=title)
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        for k, v in data.items():
            table.add_row(str(k), str(v))
        console.print(table)
    else:
        print(f"\n--- {title} ---")
        for k, v in data.items():
            print(f"{k}: {v}")
        print("-------------------")

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=['BUY', 'SELL', 'buy', 'sell'], help="Order side: BUY or SELL")
    parser.add_argument("--type", type=str, required=True, choices=['MARKET', 'LIMIT', 'market', 'limit'], help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, required=False, help="Price (required for LIMIT orders)")
    
    args = parser.parse_args()

    if has_rich:
        console = Console()
        console.print(Panel.fit("[bold blue]Binance Futures Testnet Bot[/bold blue]"))
    else:
        print("=== Binance Futures Testnet Bot ===")

    # 1. Verification of credentials
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        print_error("API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.")
        sys.exit(1)
        
    # 2. Validation
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
    except ValueError as e:
        print_error(f"Validation Error: {e}")
        logger.warning(f"Validation failed: {e}")
        sys.exit(1)
        
    # Display Order Summary Request
    req_data = {
        "Symbol": symbol,
        "Side": side,
        "Type": order_type,
        "Quantity": quantity,
    }
    if price:
        req_data["Price"] = price
        
    print_table("Order Request Summary", req_data)
    
    # 3. Execution with explicit try/except blocks
    try:
        client = BinanceFuturesClient(api_key, api_secret)
        response = place_order(client, symbol, side, order_type, quantity, price)
        
        # Display Response
        print_success("Order placed successfully!")
        
        res_data = {
            "Order ID": response.get('orderId'),
            "Status": response.get('status'),
            "Executed Qty": response.get('executedQty')
        }
        avg_price = response.get('avgPrice')
        if avg_price and float(avg_price) > 0:
            res_data["Average Price"] = avg_price
            
        print_table("Order Response Details", res_data)
        
    except BinanceAPIException as e:
        # Expected Binance API errors (network, auth, validation by Binance)
        logger.error(f"Execution Failed (API Error): {e}")
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        # Unexpected crashes
        logger.exception("Unexpected system error")
        print_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
