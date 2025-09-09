# MarketMinds

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]

MarketMinds is a lightweight **MCP (Model Context Protocol)** toolset to support financial research. It includes tools for backtesting trades, fetching market data, and retrieving company news for sentiment analysis—ideal for integrating with LLMs like Claude.

##  ✨  Features

- **BackTest Simulation** (`backtest_simulation.py`):  
  Compute historical buy/sell price performance and PnL percentage for stock symbols (via yfinance).

- **Financial Analysis Server** (`financial_analysis_server.py`):  
  An MCP server offering on-demand access to financial metrics, charts, and other market data.

- **Sentiment News Fetcher** (`sentiment_analysis.py`):  
  Fetch recent news articles for a given company using NewsAPI—perfect for feeding into LLMs for sentiment-based investing decisions.

## ⚡ Installation

Use `uv` package manager to install dependencies:

```bash
uv add fastmcp yfinance requests python-dotenv
```

Or install manually:
```bash
pip install fastmcp yfinance requests python-dotenv
```

## ⚙️ Setup
1. Create a .env file in the project root containing your NewsAPI key:
    ```bash
    NEWS_API_KEY=your_api_key_here
    ```
2. (Optional) Use pyproject.toml to define entry points or CLI commands for each tool.


## 🚀 Installing and Running MCP Tools (Installing Directly via uv run mcp install)
After creating your tools (backtest_simulation.py, financial_analysis_server.py, sentiment_analysis.py), you can register them with Claude using uv:


1. BackTest Simulation
     ```bash
    uv run mcp install backtest_simulation.py
    ```
    This command adds the Python script backtest_simulation.py to the MCP framework as a tool, enabling Claude to invoke it during its operations.
    After execution, the output will look similar to:
    ``` bash
    Added server 'BackTest_Simulation' to Claude config
    INFO Successfully installed Market_News_Fetcher in Claude app
    ```


2. Financial Analysis Server
    ```bash
    uv run mcp install financial_analysis_server.py
    ```
    This command adds the Python script financial_analysis_server.py to the MCP framework as a tool, enabling Claude to invoke it during its operations.
     After execution, the output will look similar to:
    ``` bash
    Added server 'financial_analysis' to Claude config
    INFO Successfully installed Market_News_Fetcher in Claude app
    ```

3. Sentiment News Fetcher
    ``` bash
    uv run mcp install sentiment_analysis.py
    ```
    This command adds the Python script sentiment_analysis.py to the MCP framework as a tool, enabling Claude to invoke it during its operations.
     After execution, the output will look similar to:
    ``` bash
    Added server 'Market_News_Fetcher' to Claude config
    INFO Successfully installed Market_News_Fetcher in Claude app
    ```




💡 Tip: Make sure your .env contains the NEWS_API_KEY and that it’s loaded (e.g., via python-dotenv) so the news fetcher works properly.


# Note
#### Stock Market MCP Servers (NSE + Yahoo Finance)

This is a personal study project that fetches market data using:  
- [yfinance](https://pypi.org/project/yfinance/) → for Yahoo Finance (U.S. & international stocks)  
- [nsepython](https://pypi.org/project/nsepython/) → for NSE India market data (equities, options, etc.)  

⚠️ Disclaimer:
- This project is for **educational purposes only**.
- Market data from Yahoo Finance is subject to [Yahoo Finance Terms of Service](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html).
- Market data from NSE India is subject to [NSE Terms of Use](https://www.nseindia.com/terms-of-use).
- Not intended for commercial use, trading platforms, or redistribution of data.
