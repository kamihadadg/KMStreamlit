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

def find_support_resistance(df, window=20, threshold=0.02):
    """
    Find support and resistance levels using local minima and maxima
    Returns: list of tuples (price, type, strength)
    """
    levels = []
    
    # Get local minima and maxima
    df['local_min'] = df['low'].rolling(window=window, center=True).min()
    df['local_max'] = df['high'].rolling(window=window, center=True).max()
    
    # Find support levels (local minima)
    for i in range(window, len(df) - window):
        if df['low'].iloc[i] == df['local_min'].iloc[i]:
            price = df['low'].iloc[i]
            # Check if this level is significant enough
            if not any(abs(price - level[0]) / price < threshold for level in levels):
                # Calculate strength based on number of touches
                touches = sum(1 for j in range(i-window, i+window+1) 
                            if abs(df['low'].iloc[j] - price) / price < threshold)
                levels.append((price, 'support', touches))
    
    # Find resistance levels (local maxima)
    for i in range(window, len(df) - window):
        if df['high'].iloc[i] == df['local_max'].iloc[i]:
            price = df['high'].iloc[i]
            # Check if this level is significant enough
            if not any(abs(price - level[0]) / price < threshold for level in levels):
                # Calculate strength based on number of touches
                touches = sum(1 for j in range(i-window, i+window+1) 
                            if abs(df['high'].iloc[j] - price) / price < threshold)
                levels.append((price, 'resistance', touches))
    
    # Sort levels by strength and return top 5 for each type
    support_levels = sorted([level for level in levels if level[1] == 'support'], 
                          key=lambda x: x[2], reverse=True)[:5]
    resistance_levels = sorted([level for level in levels if level[1] == 'resistance'], 
                             key=lambda x: x[2], reverse=True)[:5]
    
    return support_levels, resistance_levels 