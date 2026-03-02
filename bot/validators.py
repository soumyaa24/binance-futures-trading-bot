def validate_symbol(symbol: str) -> str:
    if not symbol or len(symbol) < 4:
        raise ValueError("Invalid symbol format. Example: BTCUSDT")
    return symbol.upper()

def validate_side(side: str) -> str:
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be either BUY or SELL")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT", "STOP_MARKET"]:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_MARKET")
    return order_type

def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    return quantity
    
def validate_price(price: float, order_type: str) -> float:
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("A positive price is required for LIMIT orders")
    return price
