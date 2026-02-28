# bot_controller.py

import threading
from tkinter import messagebox
from pybit.unified_trading import HTTP
import config
from logger import log
from bot_logic import bot_loop


def stop_bot():
    config.trade_done = True
    if not (config.bot_thread and config.bot_thread.is_alive()):
        log("Bot is not running!")
        return
    log("Bot stopped")


def start_bot(api_key_entry, api_secret_entry, testnet_var, symbol_var, 
              interval_var, candle_entry, qty_entry, buy_entry, sell_entry, marketUnit_var):
     
    config.trade_done = False
    
    if config.bot_thread and config.bot_thread.is_alive():
        log("Bot is already running!")
        return

    if not symbol_var.get():
        messagebox.showerror("Error", "No parite is chosen.")
        return

    config.apiKey = api_key_entry.get().strip()
    config.apiSecret = api_secret_entry.get().strip()
    config.testnet_mode = testnet_var.get()
    config.pariteTur = symbol_var.get()
    config.timeNumber = config.BYBIT_INTERVALS[interval_var.get()]
    config.market_unit = marketUnit_var.get()


    try:
        config.candleNumber = int(candle_entry.get())
        config.coinAmount = float(qty_entry.get())
        
        
        buy_raw = buy_entry.get().strip()
        sell_raw = sell_entry.get().strip()
        
        config.buy_percent = float(buy_raw) if buy_raw and buy_raw != "" else 0.0
        config.sell_percent = float(sell_raw) if sell_raw and sell_raw != "" else 0.0

        
        if config.buy_percent <= 0 and config.sell_percent <= 0:
            raise ValueError("At least one of the buy or sell percentages must be above 0.")

        if not (0 <= config.buy_percent < 100):
            raise ValueError("Buy percentage must be between 0-100.")
        if not (0 <= config.sell_percent < 100):
            raise ValueError("Sell percentage must be between 0-100.")

    except ValueError as e:
        messagebox.showerror("Error", f"Invalid entry: {e}")
        return


    if not config.apiKey or not config.apiSecret:
        messagebox.showerror("Error", "API information needed.")
        return


    if not config.testnet_mode:
        confirm = messagebox.askyesno("CAUTION", "You will trade with REAL MONEY! Are you sure?")
        if not confirm:
            return

    # Create session
    config.session = HTTP(
        testnet=config.testnet_mode,
        api_key=config.apiKey,
        api_secret=config.apiSecret
    )

  
    try:
        test = config.session.get_tickers(category="spot", symbol=config.pariteTur)
        if test["retCode"] == 0:
            log("API connection succesful")
        else:
            log(f"API error: {test['retMsg']}")
            return
    except Exception as e:
        log("Connection error: " + str(e))
        return

   
    t = threading.Thread(target=bot_loop, daemon=True)
    config.bot_thread = t
    t.start()

    log("Bot started")
