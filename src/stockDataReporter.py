import yfinance as yf
import matplotlib.pyplot as plt
import textwrap
import numpy as np

def create_stock_graph(ticker, period):
    # Fetch the stock data
    stock = yf.Ticker(ticker)  # Rigetti Computing
    history = stock.history(period=period)  # Get 1-year data

    # Plot the "Close" price
    plt.figure(figsize=(8, 5))
    plt.plot(history.index, history["Close"], label="Close Price", color="blue")
    plt.title(f"Stock Prices of {stock.info.get('shortName')} ({ticker}) Over {period}", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Stock Price (USD)", fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()



def compare_financial_metrics(tickers, industry_pe_ratio):
    """
    Create financial metric comparison charts for a list of companies.

    Args:
        tickers (list): List of stock ticker symbols.
        industry_pe_ratio (float): Industry average P/E ratio for comparison.

    Returns:
        None
    """
    metrics = {
        "Ticker": [],
        "P/E Ratio": [],
        "P/S Ratio": [],
        "EV/EBITDA": [],
        "P/B Ratio": []
    }

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info

        metrics["Ticker"].append(ticker)
        metrics["P/E Ratio"].append(info.get("forwardPE", np.nan))
        metrics["P/S Ratio"].append(info.get("priceToSalesTrailing12Months", np.nan))
        metrics["EV/EBITDA"].append(info.get("enterpriseToEbitda", np.nan))
        metrics["P/B Ratio"].append(info.get("priceToBook", np.nan))

    # Ensure data is consistent for plotting
    valid_indices = [i for i, pe in enumerate(metrics["P/E Ratio"]) if not np.isnan(pe)]
    for key in metrics.keys():
        if key != "Ticker":
            metrics[key] = [metrics[key][i] for i in valid_indices]
    metrics["Ticker"] = [metrics["Ticker"][i] for i in valid_indices]

    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(8, 5))
    fig.suptitle("Financial Metrics Comparison", fontsize=16)

    # Plot P/E Ratio Comparison
    axs[0, 0].bar(metrics["Ticker"], metrics["P/E Ratio"], label="Company P/E Ratio", alpha=0.7)
    axs[0, 0].axhline(y=industry_pe_ratio, color='r', linestyle='--', label="Industry Avg P/E Ratio")
    axs[0, 0].set_title("P/E Ratio Comparison")
    axs[0, 0].set_ylabel("P/E Ratio")
    axs[0, 0].legend()

    # Plot P/S Ratio Comparison
    axs[0, 1].bar(metrics["Ticker"], metrics["P/S Ratio"], color='orange')
    axs[0, 1].set_title("Price-to-Sales (P/S) Ratio Comparison")
    axs[0, 1].set_ylabel("P/S Ratio")

    # Plot EV/EBITDA Comparison
    axs[1, 0].bar(metrics["Ticker"], metrics["EV/EBITDA"], color='green')
    axs[1, 0].set_title("Enterprise Value-to-EBITDA (EV/EBITDA) Comparison")
    axs[1, 0].set_ylabel("EV/EBITDA")

    # Plot P/B Ratio Comparison
    axs[1, 1].bar(metrics["Ticker"], metrics["P/B Ratio"], color='purple')
    axs[1, 1].set_title("Price-to-Book (P/B) Ratio Comparison")
    axs[1, 1].set_ylabel("P/B Ratio")

    # Adjust layout
    for ax in axs.flat:
        ax.set_xlabel("Companies")
        ax.set_xticks(range(len(metrics["Ticker"])))
        ax.set_xticklabels(metrics["Ticker"], rotation=45, ha="right")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()



