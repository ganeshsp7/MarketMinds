from mcp.server.fastmcp import FastMCP
import yfinance as yf


mcp = FastMCP(name = "yaho_finance")

# Define MCP tool
@mcp.tool()
def get_stock_details(symbol: str) -> dict:
    """
    Fetch stock details by ticker symbol.
    Example: get_stock_details("AAPL")
    """
    sym = symbol + ".NS"
    stock = yf.Ticker(symbol)
    info = stock.info
    
    return {
        "symbol": symbol,
        "name": info.get("shortName"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "day_high": info.get("dayHigh"),
        "day_low": info.get("dayLow"),
        "currency": info.get("currency"),
    }

if __name__ == "__main__":
    mcp.run()