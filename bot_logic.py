# bot_logic.py

import time
import config
from logger import log


def bot_loop():
    while not config.trade_done:
        try:
            klines = config.session.get_kline(
                category="spot",
                symbol=config.pariteTur,
                interval=str(config.timeNumber),
                limit=config.candleNumber
            )
            
            if not klines["result"]["list"]:
                log("Candle data is empty")
                time.sleep(10)
                continue

            candles = list(reversed(klines["result"]["list"]))
            if not candles or len(candles) < 2:
                log("Insufficient candle data, waiting...")
                time.sleep(5)
                continue
                
            
            closes = [float(c[4]) for c in candles[1:]]
            if len(closes) > 0:
                close_average = sum(closes) / len(closes)
            else:
                log("No valid candle close data to calculate average.")
                time.sleep(5)
                continue

            
            response = config.session.get_tickers(
                category="spot",
                symbol=config.pariteTur
            )

            if response.get("retCode") != 0:
                log(f"Ticker error: {response.get('retMsg', 'Unkown error')}")
                time.sleep(10)
                continue

            if not response.get('result', {}).get('list'):
                log("Ticker data is empty")
                time.sleep(10)
                continue

            price = float(response['result']['list'][0]['lastPrice'])

            
            if config.buy_percent > 0 and price < close_average * ((100 - config.buy_percent) / 100):
                log(f"Price dropped {config.buy_percent}% below average. Buying...")
                place_order("Buy")
                
            
            elif config.sell_percent > 0 and price > close_average * ((100 + config.sell_percent) / 100):
                log(f"Price rose {config.sell_percent}% above average. Selling...")
                place_order("Sell")
                
            else:
                log(f"Waiting... Current: {price:.4f} | Average: {close_average:.4f}")

        except Exception as e:
            log("Error: " + str(e))

        
        for _ in range(10):
            if config.trade_done:
                break
            time.sleep(1)

    log("Bot stopped.")


def place_order(side):
    if config.trade_done:
        log("Stop request received, order not placed")
        return
    

    order_dict = {
        "category": "spot",
        "symbol": config.pariteTur,
        "side": side,
        "orderType": "Market",
        "marketUnit": config.market_unit,
        "qty": str(config.coinAmount)
    }
    


    try:
        response = config.session.place_order(**order_dict)
        order_id = response["result"]["orderId"]
        log(f"Order sent. ID: {order_id}")
        
        for _ in range(5):
            status = config.session.get_order_history(
                category="spot",
                symbol=config.pariteTur,
                orderId=order_id,
                limit=1
            )

            order_list = status.get("result", {}).get("list", [])

            if not order_list:
                log("Order not yet visible in system...")
            else:
                state = order_list[0].get("orderStatus", "Unknown")
                log(f"Order status: {state}")

                if state == "Filled":
                    log("Trade completed")
                    config.trade_done = True
                    return
                elif state in ["Cancelled", "Rejected"]:
                    log("Order failed")
                    return

            time.sleep(1)
            
    except Exception as e:
        log(f"Order error: {str(e)}")
