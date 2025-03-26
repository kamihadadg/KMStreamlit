import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import time
import numpy as np

# تنظیمات صفحه
st.set_page_config(layout="wide", page_title="Crypto Chart", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    .main {background-color: #1e1e1e; color: #d4d4d4;}
    .sidebar .sidebar-content {background-color: #252526; color: #d4d4d4;}
    .stButton>button {background-color: #3c3c3c; color: #d4d4d4;}
    .stSelectbox, .stMultiselect, .stSlider {color: #d4d4d4;}
    </style>
""", unsafe_allow_html=True)

# دیکشنری‌های متن برای دو زبان
texts_en = {
    "title": "Crypto Chart (KuCoin API)",
    "pair": "Pair",
    "timeframe": "Timeframe",
    "indicators": "Indicators",
    "ma": "MA",
    "ma_count": "Number of MAs",
    "ma_period": "MA-{i} Period",
    "macd": "MACD",
    "macd_fast": "Fast Period",
    "macd_slow": "Slow Period",
    "macd_signal": "Signal Period",
    "ichimoku": "Ichimoku",
    "tenkan": "Tenkan",
    "kijun": "Kijun",
    "senkou": "Senkou",
    "rsi": "RSI",
    "rsi_period": "RSI Period",
    "update": "Update",
    "price_label": "Price (USDT)",
    "no_data": "No data available."
}

texts_fa = {
    "title": "نمودار ارزهای دیجیتال (KuCoin API)",
    "pair": "جفت‌ارز",
    "timeframe": "تایم‌فریم",
    "indicators": "اندیکاتورها",
    "ma": "میانگین متحرک (MA)",
    "ma_count": "تعداد MA",
    "ma_period": "دوره MA-{i}",
    "macd": "مکدی (MACD)",
    "macd_fast": "دوره سریع",
    "macd_slow": "دوره کند",
    "macd_signal": "دوره سیگنال",
    "ichimoku": "ایچیموکو",
    "tenkan": "تنکان",
    "kijun": "کیجون",
    "senkou": "سنکو",
    "rsi": "آر‌اس‌آی (RSI)",
    "rsi_period": "دوره RSI",
    "update": "به‌روزرسانی",
    "price_label": "قیمت (USDT)",
    "no_data": "داده‌ای برای نمایش وجود ندارد."
}

# انتخاب زبان تو سایدبار
with st.sidebar:
    language = st.selectbox("Language / زبان", ["English", "Persian"], index=0)
    texts = texts_en if language == "English" else texts_fa

    # انتخاب جفت‌ارز
    coin_options = {
        "BTC/USDT": "BTC-USDT",
        "ETH/USDT": "ETH-USDT",
        "BNB/USDT": "BNB-USDT",
        "XRP/USDT": "XRP-USDT",
        "ADA/USDT": "ADA-USDT",
        "SOL/USDT": "SOL-USDT"
    }
    selected_coin_label = st.selectbox(texts["pair"], list(coin_options.keys()))
    selected_coin = coin_options[selected_coin_label]

    # انتخاب تایم‌فریم
    timeframe_options = {
        "1m": "1min",
        "5m": "5min",
        "15m": "15min",
        "1h": "1hour",
        "4h": "4hour",
        "1d": "1day"
    }
    selected_timeframe_label = st.selectbox(texts["timeframe"], list(timeframe_options.keys()))
    selected_timeframe = timeframe_options[selected_timeframe_label]

    # انتخاب اندیکاتورها
    indicator_options = ["MA", "MACD", "Ichimoku", "RSI"]
    selected_indicators = st.multiselect(texts["indicators"], indicator_options, default=[])

    # تنظیمات اندیکاتورها
    ma_periods = {}
    if "MA" in selected_indicators:
        st.subheader(texts["ma"])
        ma_count = st.number_input(texts["ma_count"], min_value=1, max_value=5, value=1, key="ma_count")
        for i in range(ma_count):
            ma_periods[f"MA-{i+1}"] = st.slider(texts["ma_period"].format(i=i+1), min_value=5, max_value=50, value=20 + i*5, key=f"ma_{i}")

    macd_params = {"fast": 12, "slow": 26, "signal": 9}
    if "MACD" in selected_indicators:
        st.subheader(texts["macd"])
        macd_params["fast"] = st.slider(texts["macd_fast"], min_value=5, max_value=20, value=12, key="macd_fast")
        macd_params["slow"] = st.slider(texts["macd_slow"], min_value=20, max_value=50, value=26, key="macd_slow")
        macd_params["signal"] = st.slider(texts["macd_signal"], min_value=5, max_value=20, value=9, key="macd_signal")

    if "Ichimoku" in selected_indicators:
        st.subheader(texts["ichimoku"])
        ichimoku_params = {
            "tenkan": st.slider(texts["tenkan"], min_value=5, max_value=20, value=9, key="ichimoku_tenkan"),
            "kijun": st.slider(texts["kijun"], min_value=20, max_value=50, value=26, key="ichimoku_kijun"),
            "senkou": st.slider(texts["senkou"], min_value=30, max_value=100, value=52, key="ichimoku_senkou")
        }

    rsi_period = 14
    if "RSI" in selected_indicators:
        st.subheader(texts["rsi"])
        rsi_period = st.slider(texts["rsi_period"], min_value=5, max_value=30, value=14, key="rsi_period")

    update_button = st.button(texts["update"])

# تابع دریافت داده‌ها
@st.cache_data(ttl=60)
def fetch_bitcoin_data(symbol, timeframe):
    url = "https://api.kucoin.com/api/v1/market/candles"
    params = {
        'type': timeframe,
        'symbol': symbol,
        'startAt': int(time.time()) - 60*24*3600,  # ۶۰ روز قبل
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
            return df[['timestamp', 'open', 'high', 'low', 'close']]
        else:
            st.error(f"API Error: {data['msg']}")
            return None
    except requests.RequestException as e:
        st.error(f"Data Fetch Error: {e}")
        return None

# توابع اندیکاتورها
def calculate_ma(df, period):
    return df['close'].rolling(window=period, min_periods=1).mean()

def calculate_macd(df, fast=12, slow=26, signal=9):
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def calculate_ichimoku(df, tenkan=9, kijun=26, senkou=52):
    tenkan_line = (df['high'].rolling(tenkan).max() + df['low'].rolling(tenkan).min()) / 2
    kijun_line = (df['high'].rolling(kijun).max() + df['low'].rolling(kijun).min()) / 2
    senkou_a = ((tenkan_line + kijun_line) / 2).shift(kijun)
    senkou_b = ((df['high'].rolling(senkou).max() + df['low'].rolling(senkou).min()) / 2).shift(kijun)
    chikou = df['close'].shift(-kijun)
    return tenkan_line, kijun_line, senkou_a, senkou_b, chikou

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# تابع رسم چارت
def plot_candlestick(df, indicators, ma_periods, macd_params, rsi_period, ichimoku_params):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing=dict(line=dict(color='#00ff00'), fillcolor='#00ff00'),
        decreasing=dict(line=dict(color='#ff0000'), fillcolor='#ff0000'),
        name="Candles" if language == "English" else "کندل‌ها"
    ))

    if "MA" in indicators:
        colors = ['#ffeb3b', '#ff9800', '#f44336', '#9c27b0', '#3f51b5']
        for i, (label, period) in enumerate(ma_periods.items()):
            ma_data = calculate_ma(df, period)
            fig.add_trace(go.Scatter(x=df['timestamp'], y=ma_data, line=dict(color=colors[i % len(colors)], width=2), name=label))

    if "MACD" in indicators:
        macd, signal, histogram = calculate_macd(df, macd_params["fast"], macd_params["slow"], macd_params["signal"])
        fig.add_trace(go.Scatter(x=df['timestamp'], y=macd, line=dict(color='#26a69a'), name="MACD", yaxis="y2"))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=signal, line=dict(color='#ff9800'), name="Signal" if language == "English" else "سیگنال", yaxis="y2"))
        fig.add_bar(x=df['timestamp'], y=histogram, name="Histogram" if language == "English" else "هیستوگرام", marker_color='gray', yaxis="y2")

    if "Ichimoku" in indicators:
        tenkan, kijun, senkou_a, senkou_b, chikou = calculate_ichimoku(df, ichimoku_params["tenkan"], ichimoku_params["kijun"], ichimoku_params["senkou"])
        fig.add_trace(go.Scatter(x=df['timestamp'], y=tenkan, line=dict(color='#ff0000'), name="Tenkan" if language == "English" else "تنکان"))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=kijun, line=dict(color='#0000ff'), name="Kijun" if language == "English" else "کیجون"))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=senkou_a, line=dict(color='#00ff00'), name="Senkou A" if language == "English" else "سنکو A", fill='tonexty', fillcolor='rgba(0,255,0,0.2)'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=senkou_b, line=dict(color='#ff00ff'), name="Senkou B" if language == "English" else "سنکو B", fill='tonexty', fillcolor='rgba(255,0,255,0.2)'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=chikou, line=dict(color='#00ffff'), name="Chikou" if language == "English" else "چیکو"))

    if "RSI" in indicators:
        rsi = calculate_rsi(df, rsi_period)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=rsi, line=dict(color='#ab47bc'), name="RSI", yaxis="y3"))

    fig.update_layout(
        title=f"{selected_coin_label} {selected_timeframe_label}",
        xaxis_title="",
        yaxis_title=texts["price_label"],
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1h", step="hour", stepmode="backward"),
                    dict(count=6, label="6h", step="hour", stepmode="backward"),
                    dict(count=12, label="12h", step="hour", stepmode="backward"),
                    dict(step="all", label="All" if language == "English" else "همه")
                ]),
                bgcolor="#252526",
                activecolor="#3c3c3c"
            ),
            type="date",
            showgrid=True,
            gridcolor="#444"
        ),
        yaxis=dict(
            autorange=True,
            fixedrange=False,
            showgrid=True,
            gridcolor="#444"
        ),
        dragmode="pan",
        hovermode="x unified",
        height=700,
        margin=dict(l=40, r=40, t=30, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        font=dict(color="#d4d4d4")
    )
    if "MACD" in indicators:
        fig.update_layout(
            yaxis2=dict(
                title="MACD",
                overlaying="y",
                side="right",
                position=0.85,
                showgrid=False,
                range=[macd.min() * 1.2, macd.max() * 1.2]
            )
        )
    if "RSI" in indicators:
        fig.update_layout(
            yaxis3=dict(
                title="RSI",
                overlaying="y",
                side="right",
                position=0.95,
                showgrid=False,
                range=[0, 100]
            )
        )
    fig.update_layout(
        modebar=dict(bgcolor="#1e1e1e", color="#d4d4d4", activecolor="#00ff00"),
        modebar_add=["v1hovermode", "toggleSpikelines"],
        modebar_remove=["lasso2d", "select2d"]
    )
    st.plotly_chart(fig, use_container_width=True)

# نگه‌داری داده‌ها
if ('df' not in st.session_state or 
    st.session_state.get('timeframe') != selected_timeframe or 
    st.session_state.get('coin') != selected_coin or 
    update_button):
    st.session_state.df = fetch_bitcoin_data(selected_coin, selected_timeframe)
    st.session_state.timeframe = selected_timeframe
    st.session_state.coin = selected_coin

# عنوان اصلی
st.title(texts["title"])

if st.session_state.df is not None:
    ichimoku_params = {"tenkan": 9, "kijun": 26, "senkou": 52} if "Ichimoku" not in selected_indicators else ichimoku_params
    plot_candlestick(st.session_state.df, selected_indicators, ma_periods, macd_params, rsi_period, ichimoku_params)
else:
    st.warning(texts["no_data"])