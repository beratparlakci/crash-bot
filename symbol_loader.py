# symbol_loader.py

from pybit.unified_trading import HTTP
import config
from logger import log


def init_symbols(symbol_combo=None):
    try:
        session = HTTP(testnet=True) 
        data = session.get_instruments_info(category="spot")

        config.ALL_SYMBOLS = sorted([s["symbol"] for s in data["result"]["list"]])

        log("Trading pairs loaded (public)")
        log(f"Total {len(config.ALL_SYMBOLS)} trading pairs found")

    except Exception as e:
        log("Failed to load trading pairs: " + str(e))
        config.ALL_SYMBOLS = []


def load_symbols():
    """Updates trading pair list using authenticated session"""
    try:
        data = config.session.get_instruments_info(category="spot")
        syms = sorted([s["symbol"] for s in data["result"]["list"]])
        if not syms:
            log("Trading pair list returned empty")
            return

        config.ALL_SYMBOLS = syms
        log("Trading pairs loaded from Bybit")
    except Exception as e:
        log("Failed to fetch trading pairs: " + str(e))
