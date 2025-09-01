# from mcp.server.fastmcp import FastMCP
# import yfinance as yf



# mcp = FastMCP(name = "yaho_finance")

# # Define MCP tool
# @mcp.tool()
# def get_stock_details(symbol: str) -> dict:
#     """
#     Fetch stock details by ticker symbol.
#     Example: get_stock_details("AAPL")
#     """
#     sym = symbol + ".NS"
#     stock = yf.Ticker(sym)
#     info = stock.info
    
#     return {
#         "symbol": symbol,
#         "name": info.get("shortName"),
#         "current_price": info.get("currentPrice"),
#         "market_cap": info.get("marketCap"),
#         "day_high": info.get("dayHigh"),
#         "day_low": info.get("dayLow"),
#         "currency": info.get("currency"),
#     }



# @mcp.tool()
# def get_fundamental_metrics(symbol: str) -> dict:
#     """
#     Fetch fundamental metrics of an Indian stock (NSE) by ticker symbol, including Revenue Growth.
#     Example: get_fundamental_metrics("RELIANCE")  # NSE ticker
#     Note: The symbol will automatically append '.NS' for NSE.
#     """
#     sym = symbol.upper() + ".NS"
#     stock = yf.Ticker(sym)
#     info = stock.info

#     # Financial statements
#     financials = stock.financials
#     balance_sheet = stock.balance_sheet
#     cashflow = stock.cashflow

#     # Extract key metrics with safe fallback
#     try:
#         total_assets = balance_sheet.loc["Total Assets"][0]
#         total_liabilities = balance_sheet.loc["Total Liab"][0]
#         current_assets = balance_sheet.loc["Total Current Assets"][0]
#         current_liabilities = balance_sheet.loc["Total Current Liabilities"][0]
#         operating_cashflow = cashflow.loc["Total Cash From Operating Activities"][0]
#         capital_expenditure = cashflow.loc["Capital Expenditures"][0]
#         free_cashflow = operating_cashflow - abs(capital_expenditure)
#     except Exception:
#         total_assets = total_liabilities = current_assets = current_liabilities = 0
#         operating_cashflow = capital_expenditure = free_cashflow = 0

#     # Revenue Growth Calculation (YoY)
#     try:
#         revenues = financials.loc["Total Revenue"]
#         if len(revenues) >= 2:
#             revenue_growth = (revenues[0] - revenues[1]) / revenues[1] * 100
#         else:
#             revenue_growth = None
#     except Exception:
#         revenue_growth = None

#     return {
#         "symbol": sym,
#         "name": info.get("shortName"),
#         "current_price": info.get("currentPrice"),
#         "market_cap": info.get("marketCap"),
#         "currency": info.get("currency"),

#         # Fundamental Metrics
#         "revenue_growth_percent": revenue_growth,
#         "net_profit": financials.loc["Net Income"][0] if "Net Income" in financials.index else None,
#         "operating_margin": (financials.loc["Operating Income"][0] / financials.loc["Total Revenue"][0])
#                             if "Operating Income" in financials.index and "Total Revenue" in financials.index else None,
#         "eps": info.get("trailingEps"),
#         "total_assets": total_assets,
#         "total_liabilities": total_liabilities,
#         "debt_to_equity": info.get("debtToEquity"),
#         "current_ratio": current_assets / current_liabilities if current_liabilities else None,
#         "free_cashflow": free_cashflow,
#         "operating_cashflow": operating_cashflow,
#         "pe_ratio": info.get("trailingPE"),
#         "peg_ratio": info.get("pegRatio"),
#         "pb_ratio": info.get("priceToBook"),
#         "roe": info.get("returnOnEquity"),
#         "dividend_yield": info.get("dividendYield"),
#         "revenue": financials.loc["Total Revenue"][0] if "Total Revenue" in financials.index else None,
#     }


# if __name__ == "__main__":
#     mcp.run()







from mcp.server.fastmcp import FastMCP
import yfinance as yf
import finnhub 
import os
from dotenv import load_dotenv

mcp = FastMCP(name="yahoo_finance")


# Basic stock details
# @mcp.tool()
# def get_stock_details(symbol: str) -> dict:
#     """
#     Fetch stock details by ticker symbol (NSE).
#     Example: get_stock_details("RELIANCE")
#     """
#     sym = symbol.upper() + ".NS"
#     stock = yf.Ticker(sym)
#     info = stock.info
    
#     return {
#         "symbol": symbol,
#         "name": info.get("shortName"),
#         "current_price": info.get("currentPrice"),
#         "market_cap": info.get("marketCap"),
#         "day_high": info.get("dayHigh"),
#         "day_low": info.get("dayLow"),
#         "currency": info.get("currency"),
#     }

# Fundamental metrics with growth calculations
@mcp.tool()
def get_fundamental_metrics(symbol: str) -> dict:
    """
    Fetch fundamental metrics of an Indian NSE stock for analysis.
    Includes Revenue Growth, Net Income Growth, EPS Growth, P/E, P/B, ROE, Free Cash Flow, Dividend Yield & Payout.
    Example: get_fundamental_metrics("RELIANCE")
    """
    sym = symbol.upper() + ".NS"
    stock = yf.Ticker(sym)
    info = stock.info

    # Financial statements
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow

    # Safe extraction of key metrics
    try:
        total_assets = balance_sheet.loc["Total Assets"][0]
        total_liabilities = balance_sheet.loc["Total Liab"][0]
        current_assets = balance_sheet.loc["Total Current Assets"][0]
        current_liabilities = balance_sheet.loc["Total Current Liabilities"][0]
        operating_cashflow = cashflow.loc["Total Cash From Operating Activities"][0]
        capital_expenditure = cashflow.loc["Capital Expenditures"][0]
        free_cashflow = operating_cashflow - abs(capital_expenditure)
    except Exception:
        total_assets = total_liabilities = current_assets = current_liabilities = 0
        operating_cashflow = capital_expenditure = free_cashflow = 0

    # Revenue Growth Calculation (YoY)
    try:
        revenues = financials.loc["Total Revenue"]
        revenue_growth = (revenues[0] - revenues[1]) / revenues[1] * 100 if len(revenues) >= 2 else None
    except Exception:
        revenue_growth = None

    # Net Income Growth YoY
    try:
        net_incomes = financials.loc["Net Income"]
        net_income_growth = (net_incomes[0] - net_incomes[1]) / net_incomes[1] * 100 if len(net_incomes) >= 2 else None
    except Exception:
        net_income_growth = None

    # EPS Growth YoY
    try:
        eps_values = stock.earnings['Earnings']  # yfinance earnings DataFrame
        eps_growth = (eps_values.iloc[-1] - eps_values.iloc[-2]) / eps_values.iloc[-2] * 100 if len(eps_values) >= 2 else None
    except Exception:
        eps_growth = None

    # Dividend Payout Ratio
    dividend_payout = info.get("payoutRatio")

    return {
        "symbol": sym,
        "name": info.get("shortName"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "currency": info.get("currency"),
        "day_high": info.get("dayHigh"),
        "day_low": info.get("dayLow"),

        # Fundamental Metrics
        "revenue_growth_percent": revenue_growth,
        "net_income_growth_percent": net_income_growth,
        "eps_growth_percent": eps_growth,
        "net_profit": financials.loc["Net Income"][0] if "Net Income" in financials.index else None,
        "operating_margin": (financials.loc["Operating Income"][0] / financials.loc["Total Revenue"][0])
                            if "Operating Income" in financials.index and "Total Revenue" in financials.index else None,
        "eps": info.get("trailingEps"),
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "debt_to_equity": info.get("debtToEquity"),
        "current_ratio": current_assets / current_liabilities if current_liabilities else None,
        "free_cashflow": free_cashflow,
        "operating_cashflow": operating_cashflow,
        "pe_ratio": info.get("trailingPE"),
        "peg_ratio": info.get("pegRatio"),
        "pb_ratio": info.get("priceToBook"),
        "roe": info.get("returnOnEquity"),
        "dividend_yield": info.get("dividendYield"),
        "dividend_payout_ratio": dividend_payout,
        "revenue": financials.loc["Total Revenue"][0] if "Total Revenue" in financials.index else None,
    }


if __name__ == "__main__":
    mcp.run()
