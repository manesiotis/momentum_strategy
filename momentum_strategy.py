# Momentum Strategy on S&P 500
# Author: Konstantinos Manesiotis

# Step 1: Import necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 2: Download adjusted close price data
tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'JNJ', 'V',
    'PG', 'UNH', 'MA', 'HD', 'DIS', 'KO', 'PEP', 'MRK', 'ABBV', 'CVX',
    'BAC', 'PFE', 'INTC', 'T', 'CSCO', 'WMT', 'XOM', 'ADBE', 'VZ', 'NFLX',
    'ORCL', 'CMCSA', 'NKE', 'ABT', 'COST', 'MCD', 'MDT', 'CRM', 'TXN', 'LLY',
    'UPS', 'PM', 'MS', 'NEE', 'QCOM', 'AMGN', 'UNP', 'IBM', 'TMO', 'GS'
]

start_date = "2015-01-01"
end_date = "2024-12-31"

# Download data
data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)['Adj Close']

# Drop stocks with missing data
data = data.dropna(axis=1)

# Save to CSV (optional)
data.to_csv("data/clean_prices.csv")

# Step 3: Calculate momentum and select top-N stocks each month

# Convert daily prices to monthly prices (last trading day of each month)
monthly_prices = data.resample('ME').last()

# Calculate monthly returns (used later in backtesting)
monthly_returns = monthly_prices.pct_change()

# Calculate 12-month momentum: percentage return from t-13 to t-1
# Shift by 1 month to avoid using future information (look-ahead bias)
momentum = monthly_prices.pct_change(periods=12).shift(1)

# Rank the stocks each month based on momentum (higher return = higher rank)
momentum_rankings = momentum.rank(axis=1, ascending=False)

# Define how many top momentum stocks to select
top_n = 10

# Get a list of the top-N tickers for each month
top_n_stocks = momentum_rankings.apply(lambda x: x[x <= top_n].index.tolist(), axis=1)

# Print an example: top momentum stocks in January 2020
print(f"Top {top_n} momentum stocks in 2020-01:")
print(top_n_stocks.loc['2020-01-31'])

# Step 4: Simple backtest for the momentum strategy

# Initialize an empty series to store portfolio returns
portfolio_returns = pd.Series(dtype=float)

# Loop over each month starting from the first valid month
for date in top_n_stocks.index[1:]:
    # Get top-N stocks for this month
    selected_stocks = top_n_stocks.loc[date]
    
    # Ensure selected stocks have return data
    available_stocks = [stock for stock in selected_stocks if stock in monthly_returns.columns]
    
    # Get the returns of these stocks for the *next* month (i.e., after selection)
    try:
        next_month = monthly_returns.index[monthly_returns.index.get_loc(date) + 1]
        returns = monthly_returns.loc[next_month, available_stocks]
        portfolio_return = returns.mean()  # Equal-weighted
        portfolio_returns.loc[next_month] = portfolio_return
    except (IndexError, KeyError):
        continue  # Skip if next month is out of range or data missing

# Step 5: Calculate and plot cumulative performance

# Compute cumulative returns
cumulative_returns = (1 + portfolio_returns).cumprod()

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(cumulative_returns, label='Momentum Strategy', linewidth=2)

# Optional: add benchmark (e.g. SPY ETF)
benchmark = yf.download('SPY', start=start_date, end=end_date, auto_adjust=False)['Adj Close'].resample('ME').last().pct_change()
benchmark_cum = (1 + benchmark).cumprod()
plt.plot(benchmark_cum, label='S&P 500 (SPY)', linestyle='--')

plt.title('Momentum Strategy vs S&P 500')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True)

# Save plot to file
plt.savefig("plots/momentum_vs_sp500.png")
plt.show()








