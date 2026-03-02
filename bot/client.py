import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from bot.logging_config import logger

class BinanceAPIException(Exception):
    """Custom exception for Binance API errors."""
    pass

class BinanceFuturesClient:
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })
        
    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
    def _request(self, method: str, endpoint: str, params: dict = None):
        if params is None:
            params = {}
            
        params['timestamp'] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        
        url = f"{self.BASE_URL}{endpoint}?{query_string}&signature={signature}"
        
        # LOGGING REQUEST PAYLOAD
        logger.info(f"API Request - Method: {method} | Endpoint: {endpoint} | Payload/Params: {params}")
        
        try:
            response = self.session.request(method, url)
            response.raise_for_status()
            data = response.json()
            # LOGGING SUCCESS RESPONSE
            logger.info(f"API Response Summary - Endpoint: {endpoint} | Status: {response.status_code}")
            logger.info(f"API Response Data: {data}")
            return data
        except requests.exceptions.HTTPError as err:
            try:
                error_data = err.response.json()
                msg = f"Binance Error: {error_data.get('msg', 'Unknown')} (Code: {error_data.get('code', 'Unknown')})"
            except Exception:
                msg = err.response.text
            # TRACEBACK / EXCEPTION LOGGING
            logger.error(f"HTTPError Payload: {params}")
            logger.exception(f"HTTP Error: {err.response.status_code} - {msg}")
            raise BinanceAPIException(msg) from err
        except requests.exceptions.ConnectionError as err:
            logger.exception(f"Network Error: {err}")
            raise BinanceAPIException("Failed to connect to Binance API (Network Error).") from err
        except requests.exceptions.Timeout as err:
            logger.exception(f"Network Timeout Error: {err}")
            raise BinanceAPIException("Request to Binance API timed out.") from err
        except Exception as err:
            logger.exception(f"Unexpected Exception occurred: {err}")
            raise BinanceAPIException(f"An unexpected error occurred: {str(err)}") from err
