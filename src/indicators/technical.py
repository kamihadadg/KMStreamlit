import pandas as pd
import numpy as np

def calculate_ma(df, period):
    """Calculate Moving Average"""
    return df['close'].rolling(window=period, min_periods=1).mean()

def calculate_macd(df, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def calculate_ichimoku(df, tenkan=9, kijun=26, senkou=52):
    """Calculate Ichimoku Cloud indicators"""
    tenkan_line = (df['high'].rolling(tenkan).max() + df['low'].rolling(tenkan).min()) / 2
    kijun_line = (df['high'].rolling(kijun).max() + df['low'].rolling(kijun).min()) / 2
    senkou_a = ((tenkan_line + kijun_line) / 2).shift(kijun)
    senkou_b = ((df['high'].rolling(senkou).max() + df['low'].rolling(senkou).min()) / 2).shift(kijun)
    chikou = df['close'].shift(-kijun)
    return tenkan_line, kijun_line, senkou_a, senkou_b, chikou

def calculate_rsi(df, period=14):
    """Calculate RSI (Relative Strength Index)"""
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_volume_profile(df, bins=10):
    """Calculate Volume Profile"""
    price_bins = pd.qcut(df['close'], q=bins, duplicates='drop')
    volume_profile = df.groupby(price_bins)['volume'].sum()
    return volume_profile 