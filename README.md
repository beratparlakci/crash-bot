### Note:
The commit history has been cleaned and the project has been restarted as an "initial commit".
This was done to make the project more readable and easier to understand.



# Crash Bot

Monitors Bybit spot prices and places buy/sell orders when the price moves a set percentage away from the recent candle average.

---

## How it works

The bot fetches the last N candles for a given symbol and calculates the average closing price. If the live price drops X% below that average, it buys. If it rises Y% above, it sells. After a trade is filled the bot stops — one trade per run.

---

## Setup

Requires Python 3.9 or higher.

```bash
git clone https://github.com/beratparlakci/crash-bot.git
cd crash-bot
pip install -r requirements.txt
python main.py
```

---

## Usage

Fill in your API credentials, pick a symbol, set your candle count and interval, then configure the buy/sell thresholds and quantity. Leave Testnet Mode on until you're confident everything works as expected.

A few things worth knowing:
- At least one of Buy % or Sell % must be greater than zero
- Market Unit: use `quoteCoin` if you want to spend/receive USDT, `baseCoin` for the asset itself
- The bot stops automatically once an order is filled

---

## Project layout

```
Project Layout
├── main.py            # Entry point of the application
├── gui.py             # CustomTkinter interface and UI elements
├── bot_controller.py  # Thread management and start/stop logic
├── bot_logic.py       # Core strategy, price checks, and order placement
├── config.py          # Shared state, API keys, and global settings
├── logger.py          # Real-time log output system for the GUI
├── symbol_loader.py   # Fetches and filters available symbols from Bybit
├── requirements.txt   # Project dependencies
└── README.md          # Documentation

```

## Disclaimer

This is a personal tool provided for educational and informational purposes only. It does not constitute financial or investment advice.

By using this software, you acknowledge and accept that cryptocurrency trading involves substantial risk, including the potential loss of all funds. You agree that you are solely responsible for your trading decisions and any resulting profits or losses.

The author provides this software "as is", without any warranties or guarantees of performance, profitability, or reliability, and shall not be held liable for any financial losses, damages, or consequences arising from its use.

Only use money you can afford to lose.

---

## License

MIT
