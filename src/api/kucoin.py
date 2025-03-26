import requests
import pandas as pd
import time
import streamlit as st

@st.cache_data(ttl=60)
def fetch_candles(symbol, timeframe):
    """Fetch candle data from KuCoin API"""
    url = "https://api.kucoin.com/api/v1/market/candles"
    params = {
        'type': timeframe,
        'symbol': symbol,
        'startAt': int(time.time()) - 60*24*3600,
        'endAt': int(time.time())
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['code'] == '200000':
            df = pd.DataFrame(data['data'], columns=['timestamp', 'open', 'close', 'high', 'low', 'volume', 'amount'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df['open'] = pd.to_numeric(df['open'], errors='coerce')
            df['close'] = pd.to_numeric(df['close'], errors='coerce')
            df['high'] = pd.to_numeric(df['high'], errors='coerce')
            df['low'] = pd.to_numeric(df['low'], errors='coerce')
            df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        else:
            st.error(f"API Error: {data['msg']}")
            return None
    except requests.RequestException as e:
        st.error(f"Data Fetch Error: {e}")
        return None

@st.cache_data(ttl=60)
def fetch_market_info(symbol):
    """Fetch market statistics from KuCoin API"""
    url = "https://api.kucoin.com/api/v1/market/stats"
    params = {'symbol': symbol}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['code'] == '200000':
            return data['data']
        return None
    except:
        return None 