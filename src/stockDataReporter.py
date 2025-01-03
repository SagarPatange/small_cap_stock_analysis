import yfinance as yf
import matplotlib.pyplot as plt
import textwrap

def create_stock_graph(ticker, period):
    # Fetch the stock data
    stock = yf.Ticker(ticker)  # Rigetti Computing
    history = stock.history(period=period)  # Get 1-year data

    # Plot the "Close" price
    plt.figure(figsize=(10, 6))
    plt.plot(history.index, history["Close"], label="Close Price", color="blue")
    plt.title(f"Stock Prices of {stock.info.get("shortName")} ({ticker}) Over {period}", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Stock Price (USD)", fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()

