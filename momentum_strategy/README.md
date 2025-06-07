# Momentum Trading Strategy on S&P 500

This project implements a **momentum-based trading strategy** using historical price data from S&P 500 stocks. The strategy selects and invests in the top-performing stocks based on their past 12-month returns, excluding the most recent month, and rebalances the portfolio monthly.

---

## 📈 Strategy Overview

**Momentum effect** is the tendency of stocks that have performed well in the past to continue performing well in the near future.

### Steps:
1. **Download data** for 50 large-cap stocks from the S&P 500.
2. **Resample to monthly data** and calculate 12-month returns (momentum).
3. **Each month**, rank all stocks by momentum and select the top-N (e.g. top 10).
4. **Invest equal weight** in selected stocks and hold for 1 month.
5. **Repeat** the process every month (monthly rebalancing).

---

## 🧪 Backtest Setup

- **Universe**: 50 large-cap S&P 500 stocks
- **Period**: 2015–2024
- **Rebalancing**: Monthly
- **Holding period**: 1 month
- **Momentum window**: 12-month return, skipping the most recent month
- **Benchmark**: SPY ETF (S&P 500 index)

---

## 📊 Results

- The strategy's cumulative return is plotted and compared to the S&P 500 index.
- Returns are calculated using a **simple equal-weighted allocation**.
- Data is adjusted for splits and dividends using Yahoo Finance (`yfinance`).

<p align="center">
  <img src="plots/momentum_vs_sp500.png" alt="Momentum vs SPY" width="700">
</p>

---

## 🛠 Libraries Used

- `pandas`
- `numpy`
- `yfinance`
- `matplotlib`

---

## 📁 Project Structure

- momentum-trading-strategy/
  - momentum_strategy.py          # Main strategy code
  - data/
    - clean_prices.csv            # Cleaned stock price data
  - plots/
    - momentum_vs_sp500.png       # Cumulative return chart
  - README.md                     # Project description and results

## ⚠️ Disclaimer

This project is for educational purposes only. It does not constitute financial advice or an investment recommendation.


