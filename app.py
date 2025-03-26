import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# عنوان اپلیکیشن
st.title("نمودار زنده قیمت بیت‌کوین (Binance API)")

# تابع برای دریافت داده‌های قیمت بیت‌کوین از Binance API
def fetch_bitcoin_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': 'BTCUSDT',  # جفت ارز BTC/USDT
        'interval': '1h',     # بازه زمانی هر ۱ ساعت
        'limit': 24           # تعداد داده‌ها (۲۴ داده برای ۲۴ ساعت گذشته)
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
            'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
            'taker_buy_quote_asset_volume', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['close'] = df['close'].astype(float)  # تبدیل قیمت بسته‌شدن به عدد
        return df[['timestamp', 'close']]  # بازگشت زمان و قیمت بسته‌شدن
    else:
        st.error("خطا در دریافت داده‌ها از Binance API")
        return None

# نمایش داده‌ها در یک نمودار
def plot_data(df):
    fig = px.line(df, x='timestamp', y='close', title='قیمت بیت‌کوین در ۲۴ ساعت گذشته (Binance)')
    st.plotly_chart(fig)

# به‌روزرسانی خودکار داده‌ها
def auto_refresh(interval=60):  # هر ۶۰ ثانیه به‌روزرسانی شود
    while True:
        df = fetch_bitcoin_data()
        if df is not None:
            plot_data(df)
        time.sleep(interval)

# اجرای اپلیکیشن
if __name__ == "__main__":
    auto_refresh()