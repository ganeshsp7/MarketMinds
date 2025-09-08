from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

mcp = FastMCP(name="Market_News_Fetcher")

# load .env file into environment
load_dotenv()

NEWSAPI_KEY = os.getenv("NEWS_API_KEY")  

def fetch_company_news(company: str, limit: int = 5):
    """
    Fetch latest news articles about a company using NewsAPI.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": limit,
        "apiKey": NEWSAPI_KEY,
    }

    resp = requests.get(url, params=params)
    data = resp.json()

    if data.get("status") != "ok":
        return {"error": data.get("message", "Unknown error")}

    return data.get("articles", [])


@mcp.tool()
def Company_News(company: str, limit: int = 5) -> dict:
    """
    Fetch latest news of a given company so LLM can analyze sentiment or other insights to support investment decisions.

    Args:
        company (str): Company name (e.g., "Tesla", "Apple").
        limit (int): Number of articles (default=5).

    Returns:
        dict: {
            "company": str,
            "articles": [
                {"title": str, "url": str, "description": str, "publishedAt": str}
            ]
        }
    """
    articles = fetch_company_news(company, limit)
    # Ensure we got a list of dicts
    if not isinstance(articles, list):
        return {"error": f"Unexpected response: {articles}"}
    
    results = []
    for art in articles:
        results.append({
            "title": art.get("title", ""),
            "url": art.get("url", ""),
            "description": art.get("description", ""),
            "publishedAt": art.get("publishedAt", "")
        })

    return {"company": company, "articles": results}


if __name__ == "__main__":
    mcp.run()
