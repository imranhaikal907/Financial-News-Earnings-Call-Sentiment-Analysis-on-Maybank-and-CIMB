import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

start_date = "2023-01-01"
end_date = "2023-11-01"
maybank = yf.download("1155.KL", start=start_date, end=end_date)
cimb = yf.download("1023.KL", start=start_date, end=end_date)
klci = yf.download("^KLSE", start=start_date, end=end_date)  # Benchmark

maybank['Return'] = maybank['Close'].pct_change()
cimb['Return'] = cimb['Close'].pct_change()
klci['Return'] = klci['Close'].pct_change()

window = 20  # 20 trading days ~ 1 month
maybank['Volatility'] = maybank['Return'].rolling(window).std() * np.sqrt(window)  # Annualized volatility
cimb['Volatility'] = cimb['Return'].rolling(window).std() * np.sqrt(window)

def calculate_beta(stock_returns, benchmark_returns, window=60):  # 60-day rolling beta
    cov = stock_returns.rolling(window).cov(benchmark_returns)
    var = benchmark_returns.rolling(window).var()
    beta = cov / var
    return beta
maybank['Beta'] = calculate_beta(maybank['Return'], klci['Return'])
cimb['Beta'] = calculate_beta(cimb['Return'], klci['Return'])

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(14, 10))
# 1. Closing Prices
plt.subplot(3, 1, 1)
plt.plot(maybank.index, maybank['Close'], label='Maybank')
plt.plot(cimb.index, cimb['Close'], label='CIMB')
plt.title('Adjusted Closing Prices')
plt.ylabel('Price (MYR)')
plt.legend()
plt.grid(True)
# 2. Rolling Volatility (Annualized)
plt.subplot(3, 1, 2)
plt.plot(maybank.index, maybank['Volatility'], label='Maybank')
plt.plot(cimb.index, cimb['Volatility'], label='CIMB')
plt.title('Rolling 20-Day Annualized Volatility')
plt.ylabel('Volatility')
plt.legend()
plt.grid(True)
# 3. Rolling Beta (Market Sensitivity)
plt.subplot(3, 1, 3)
plt.plot(maybank.index, maybank['Beta'], label='Maybank')
plt.plot(cimb.index, cimb['Beta'], label='CIMB')
plt.title('Rolling 60-Day Beta vs KLCI')
plt.ylabel('Beta')
plt.xlabel('Date')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

import yfinance as yf
import numpy as np
import pandas as pd

# Ensure maybank DataFrame is downloaded and processed if not already in memory
try:
    maybank_summary = maybank.describe()
except NameError:
    print('maybank variable not found in memory. Fetching and preparing data...')
    start_date = '2023-01-01'
    end_date = '2023-11-01'
    maybank = yf.download('1155.KL', start=start_date, end=end_date)
    klci = yf.download('^KLSE', start=start_date, end=end_date)

    maybank['Return'] = maybank['Close'].pct_change()
    klci['Return'] = klci['Close'].pct_change()

    window = 20
    maybank['Volatility'] = maybank['Return'].rolling(window).std() * np.sqrt(window)

    cov = maybank['Return'].rolling(60).cov(klci['Return'])
    var = klci['Return'].rolling(60).var()
    maybank['Beta'] = cov / var

    maybank_summary = maybank.describe()

# display(maybank_summary)

# Keep index=True so the summary statistics labels (count, mean, std, etc.) are included in the Excel file
# This also avoids the NotImplementedError associated with MultiIndex columns and index=False
maybank_summary.to_excel("comp_equityrisk.xlsx", index=True)