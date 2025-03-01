import ccxt
import pandas as pd
import time
import matplotlib.pyplot as plt

exchange = ccxt.binance()

# Fetch market data
def fetch_market_data(symbol, timeframe='1m', limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Compute volatility & liquidity
def analyze_market(df):
    df['returns'] = df['close'].pct_change()
    df['volatility'] = df['returns'].rolling(20).std()
    df['spread'] = (df['high'] - df['low']) / df['close']
    return df

symbol = 'BTC/USDT'
df = fetch_market_data(symbol)
df = analyze_market(df)

# Plot volatility & spread
plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
plt.plot(df['timestamp'], df['volatility'], label='Volatility')
plt.legend()

plt.subplot(2,1,2)
plt.plot(df['timestamp'], df['spread'], label='Spread', color='red')
plt.legend()
plt.show()

