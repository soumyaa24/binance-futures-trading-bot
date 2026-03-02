from bot.client import BinanceFuturesClient
from bot.logging_config import logger

def place_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    endpoint = "/fapi/v1/order"
    
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
    }
    
    if order_type.upper() == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        params["price"] = price
        params["timeInForce"] = "GTC" # Good Till Cancel
        
    logger.info(f"Preparing to place {order_type} order for {quantity} {symbol} ({side})")
    
    try:
        response = client._request("POST", endpoint, params)
        logger.info(f"Order successfully placed. Order ID: {response.get('orderId')}")
        return response
    except Exception as e:
        logger.error(f"Failed to place order: {str(e)}")
        raise
