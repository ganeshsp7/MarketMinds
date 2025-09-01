# from mcp.server.fastmcp import FastMCP
# import finnhub 
# import os
# from dotenv import load_dotenv

# mcp = FastMCP(name="News_sentiment_analysis")

# # Load environment variables from .env file
# load_dotenv()

# # Get API key from environment
# FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

# # Setup client
# finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


# # Market News Tool
# @mcp.tool()
# def get_company_news(symbol: str, days: int = 15) -> list:
#     """
#     Fetch latest company-specific news for a given stock ticker (NSE).
#     Example: get_company_news("RELIANCE", days=15)
#     """
#     import datetime

#     sym = symbol.upper() + ".NS"

#     # Date range
#     today = datetime.date.today()
#     start_date = today - datetime.timedelta(days=days)

#     # Fetch company news from Finnhub (works on global symbols, so strip .NS for API call)
#     news = finnhub_client.company_news(
#         sym,
#         _from=str(start_date),
#         to=str(today)
#     )

#     # Format top 5 headlines
#     latest_news = []
#     for item in news[:5]:
#         latest_news.append({
#             "headline": item.get("headline"),
#             "datetime": datetime.datetime.fromtimestamp(item["datetime"]).strftime("%Y-%m-%d %H:%M"),
#             "source": item.get("source"),
#             "url": item.get("url")
#         })

#     return {
#         "symbol": symbol,
#         "news_count": len(news),
#         "latest_news": latest_news
#     }



# if __name__ == "__main__":
#     mcp.run()