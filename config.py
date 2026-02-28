# config.py

BYBIT_INTERVALS = {
    "1m": "1",
    "3m": "3",
    "5m": "5",
    "15m": "15",
    "30m": "30",
    "1h": "60",
    "2h": "120",
    "4h": "240",
    "6h": "360",
    "12h": "720",
    "1d": "D",  
    "1w": "W",  
    "1M": "M",    
}

apiKey = None
apiSecret = None
candleNumber = None
timeNumber = None
pariteTur = None
coinAmount = None
trade_done = False
testnet_mode = True
buy_percent = None
sell_percent = None
bot_thread = None
session = None
market_unit = None
ALL_SYMBOLS = []
