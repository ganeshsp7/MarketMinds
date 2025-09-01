# from mcp.server.fastmcp import FastMCP
# import yfinance as yf
# import os
# from dotenv import load_dotenv
# import pandas as pd
# from datetime import datetime

# mcp = FastMCP(name="BackTest_Simulation")


# def get_price_on_date(ticker: str, date: str, price_type: str = "Close"):
#     """
#     Fetch price of a ticker on a specific date using yfinance.
#     If date is in the past → return closing price of that date.
#     If date is today → return latest available price.
#     """
#     stock = yf.Ticker(ticker)
#     target_date = pd.to_datetime(date).date()
#     today = datetime.today().date()

#     # Case 1: Historic date (before today) → return closing price
#     if target_date < today:
#         next_day = pd.to_datetime(date) + pd.Timedelta(days=1)
#         hist = stock.history(start=date, end=next_day.strftime("%Y-%m-%d"))
#         if hist.empty:
#             return None  # market closed
#         return hist["Close"].iloc[0]

#     # Case 2: Today → return latest available price
#     elif target_date == today:
#         live = stock.history(period="1d", interval="1m")  # latest intraday
#         if live.empty:
#             return None
#         return live["Close"].iloc[-1]

#     # Future dates → not possible
#     else:
#         return None
    

# # Backtest_Simulation
# @mcp.tool()
# def BackTest_Simulation_Tool(ticker: str, buy_date: str, sell_date: str = None) -> dict:    
#     """
#     BackTest_Simulation_Tool: Get buy & sell prices for backtesting.

#     Args:
#         ticker (str): Stock symbol (e.g., 'HDFCBANK.NS')
#         buy_date (str): Buy date in 'YYYY-MM-DD'
#         sell_date (str): Sell date in 'YYYY-MM-DD' (default = today)

#     Returns:
#         dict: { "buy_date": price, "sell_date": price }
#     """

#     buy_price = get_price_on_date(ticker, buy_date)
#     sell_price = get_price_on_date(ticker, sell_date)

#     return {
#         "buy_date": buy_price,
#         "sell_date": sell_price
#     }


# if __name__ == "__main__":
#     mcp.run()























from mcp.server.fastmcp import FastMCP
import yfinance as yf
import pandas as pd
from datetime import datetime

mcp = FastMCP(name="BackTest_Simulation")


def get_price_on_date(ticker: str, date: str, price_type: str = "Close"):
    """
    Fetch price of a ticker on a specific date using yfinance.
    If date is in the past → return closing price of that date.
    If date is today → return latest available price.
    If date falls on a holiday/weekend → returns next available close.
    """
    stock = yf.Ticker(ticker)
    target_date = pd.to_datetime(date).date()
    today = datetime.today().date()

    # Case 1: Historic date (before today)
    if target_date < today:
        end_date = (pd.to_datetime(date) + pd.Timedelta(days=5)).strftime("%Y-%m-%d")
        hist = stock.history(start=date, end=end_date)
        if hist.empty:
            return None
        return hist[price_type].iloc[0]  # first available close

    # Case 2: Today → latest intraday
    elif target_date == today:
        live = stock.history(period="1d", interval="1m")
        if live.empty:
            return None
        return live[price_type].iloc[-1]

    # Future dates → not possible
    else:
        return None
    

@mcp.tool()
def BackTest_Simulation_Tool(ticker: str, buy_date: str, sell_date: str = None) -> dict:    
    """
    BackTest_Simulation_Tool: Get buy & sell prices for backtesting.

    Args:
        ticker (str): Stock symbol (e.g., 'HDFCBANK.NS')
        buy_date (str): Buy date in 'YYYY-MM-DD'
        sell_date (str): Sell date in 'YYYY-MM-DD' (default = today)

    Returns:
        dict: { "ticker": str, "buy_date": str, "buy_price": float,
                "sell_date": str, "sell_price": float, "pnl_pct": float }
    """
    if sell_date is None:
        sell_date = datetime.today().strftime("%Y-%m-%d")

    buy_price = get_price_on_date(ticker, buy_date)
    sell_price = get_price_on_date(ticker, sell_date)

    pnl_pct = None
    if buy_price and sell_price:
        pnl_pct = ((sell_price - buy_price) / buy_price) * 100

    return {
        "ticker": ticker,
        "buy_date": buy_date,
        "buy_price": buy_price,
        "sell_date": sell_date,
        "sell_price": sell_price,
        "pnl_pct": pnl_pct
    }


if __name__ == "__main__":
    mcp.run()
