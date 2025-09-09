from mcp.server.fastmcp import FastMCP
import yfinance as yf
from nsepython import nse_optionchain_scrapper
import json


mcp = FastMCP(name="option_chain_analysis")


@mcp.tool()
def option_chain_data(symbol: str) -> dict:
    """
    Fetches the option chain data for a given NSE stock symbol and returns information 
    for the first available expiry date.

    Parameters:
    -----------
    symbol : str
        The NSE stock symbol (e.g., "INFY", "RELIANCE").

    Returns:
    --------
    dict
        A dictionary containing:
        - 'symbol': The stock symbol.
        - 'expiry': The first available option expiry date.
        - 'data': A list of option chain entries (calls and puts) for the first expiry.

    Notes:
    ------
    - Each item in 'data' includes CE (Call) and PE (Put) option details.
    - This function is useful for analyzing options, identifying potential support 
      and resistance levels, and other derivatives-related calculations.
    """
    # Fetch F&O data
    fno_data = nse_optionchain_scrapper(symbol)

    # Check if records or expiryDates exist
    if 'records' not in fno_data or not fno_data['records'].get('expiryDates'):
        return {"symbol": symbol, "message": "No F&O data available."}
    
    # Get the first expiry date
    first_expiry = fno_data['records']['expiryDates'][0]

    # Total option chain data
    option_data = fno_data['records']['data']

    # Filter data matching the first expiry
    first_expiry_data = [item for item in option_data if item['expiryDate'] == first_expiry]

    # Print the first expiry option data (optional, for debugging)
    # for option in first_expiry_data:
    #     print(option)
    print(type(first_expiry_data))

    # Return as a dict
    return json.dumps({
        "symbol": symbol,
        "expiry": first_expiry,
        "data": first_expiry_data
    }, default=str)  # converts non-serializable objects to strings


if __name__ == "__main__":
    # mcp.run()
    option_chain_data("INFY")
