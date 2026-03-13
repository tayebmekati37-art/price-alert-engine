import requests
import yfinance as yf
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# CoinGecko API endpoint for crypto prices (no API key required)
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

def fetch_crypto_price(symbol: str) -> Optional[float]:
    try:
        params = {
            'ids': symbol.lower(),
            'vs_currencies': 'usd'
        }
        response = requests.get(COINGECKO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if symbol.lower() in data:
            return data[symbol.lower()]['usd']
        else:
            logger.error(f"Symbol {symbol} not found in CoinGecko response")
            return None
    except Exception as e:
        logger.error(f"Error fetching crypto price for {symbol}: {e}")
        return None

def fetch_stock_price(symbol: str) -> Optional[float]:
    try:
        ticker = yf.Ticker(symbol.upper())
        if hasattr(ticker, 'fast_info') and ticker.fast_info is not None:
            price = ticker.fast_info['lastPrice']
            if price is not None:
                return float(price)
        hist = ticker.history(period="1d", interval="1m")
        if not hist.empty:
            return float(hist['Close'].iloc[-1])
        logger.error(f"No price data for stock {symbol}")
        return None
    except Exception as e:
        logger.error(f"Error fetching stock price for {symbol}: {e}")
        return None

def fetch_price(asset_type: str, symbol: str) -> Optional[float]:
    if asset_type == 'crypto':
        return fetch_crypto_price(symbol)
    elif asset_type == 'stock':
        return fetch_stock_price(symbol)
    else:
        logger.error(f"Unknown asset type: {asset_type}")
        return None
