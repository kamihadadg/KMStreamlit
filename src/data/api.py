import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz

def fetch_candles(symbol, timeframe):
    """Fetch candlestick data from KuCoin API"""
    try:
        # Convert timeframe to seconds
        timeframe_seconds = {
            "1m": 60,
            "5m": 300,
            "15m": 900,
            "30m": 1800,
            "1h": 3600,
            "4h": 14400,
            "1d": 86400,
            "1w": 604800
        }
        
        # Calculate start and end time
        end_time = int(datetime.now().timestamp())
        start_time = end_time - (timeframe_seconds[timeframe] * 200)  # Get last 200 candles
        
        # Make API request
        url = f"https://api.kucoin.com/api/v1/market/candles?symbol={symbol}&type={timeframe}&startAt={start_time}&endAt={end_time}"
        response = requests.get(url)
        data = response.json()
        
        if data["code"] == "200000":
            # Convert data to DataFrame
            df = pd.DataFrame(data["data"], columns=["timestamp", "open", "close", "high", "low", "volume", "turnover"])
            
            # Convert timestamp to datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="s")
            
            # Convert string values to float
            for col in ["open", "close", "high", "low", "volume", "turnover"]:
                df[col] = df[col].astype(float)
            
            # Sort by timestamp
            df = df.sort_values("timestamp")
            
            return df
        else:
            return None
    except Exception as e:
        print(f"Error fetching candles: {e}")
        return None

def fetch_market_info(symbol):
    """Fetch market information from KuCoin API"""
    try:
        # Make API request
        url = f"https://api.kucoin.com/api/v1/market/stats?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        
        if data["code"] == "200000":
            return data["data"]
        else:
            return None
    except Exception as e:
        print(f"Error fetching market info: {e}")
        return None

def find_support_resistance(df, window=20, price_threshold=0.02, strength_threshold=2):
    """Find support and resistance levels using price action"""
    support_levels = []
    resistance_levels = []
    
    for i in range(window, len(df) - window):
        # Get the current window
        current_window = df.iloc[i-window:i+window]
        current_price = df.iloc[i]["close"]
        
        # Find local minimums and maximums
        is_support = all(current_price <= df.iloc[i-j]["low"] for j in range(1, window)) and \
                    all(current_price <= df.iloc[i+j]["low"] for j in range(1, window))
        
        is_resistance = all(current_price >= df.iloc[i-j]["high"] for j in range(1, window)) and \
                       all(current_price >= df.iloc[i+j]["high"] for j in range(1, window))
        
        # Calculate level strength based on touches
        if is_support or is_resistance:
            touches = 0
            for j in range(i+1, len(df)):
                price_range = current_price * price_threshold
                if df.iloc[j]["low"] >= current_price - price_range and \
                   df.iloc[j]["high"] <= current_price + price_range:
                    touches += 1
            
            # Add level if it has enough touches
            if touches >= strength_threshold:
                level = (current_price, i, touches)
                if is_support:
                    support_levels.append(level)
                else:
                    resistance_levels.append(level)
    
    return support_levels, resistance_levels 