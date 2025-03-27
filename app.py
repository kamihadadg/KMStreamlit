import streamlit as st
import pandas as pd
from src.config.settings import setup_page_config, get_styles
from src.config.texts import get_texts
from src.api.kucoin import fetch_candles
from src.ui.chart import plot_candlestick
import time
import random

# Page configuration
setup_page_config()
st.markdown(get_styles(), unsafe_allow_html=True)

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = "English"
if 'theme' not in st.session_state:
    st.session_state.theme = "Dark"
if 'show_grid' not in st.session_state:
    st.session_state.show_grid = True
if 'show_crosshair' not in st.session_state:
    st.session_state.show_crosshair = True
if 'timezone' not in st.session_state:
    st.session_state.timezone = "UTC"
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'indicators' not in st.session_state:
    st.session_state.indicators = {
        'MA': [],
        'MACD': [],
        'RSI': [],
        'Ichimoku': []
    }

# Get texts based on language
texts = get_texts(st.session_state.language)

# Auto-refresh logic
if st.session_state.auto_refresh:
    current_time = time.time()
    if current_time - st.session_state.last_refresh >= 60:  # 60 seconds = 1 minute
        st.session_state.last_refresh = current_time
        st.rerun()

# Sidebar
with st.sidebar:
    st.title(texts["title"])
    st.markdown(texts["subtitle"])
    
    # Language and Theme selection in one row
    col1, col2 = st.columns(2)
    with col1:
        st.caption(texts["language"])
        language = st.selectbox("", ["English", "Persian", "German"], key="language_select", label_visibility="collapsed")
        if language != st.session_state.language:
            st.session_state.language = language
            texts = get_texts(language)
    
    with col2:
        st.caption(texts["theme"])
        theme = st.selectbox("", [texts["dark"], texts["light"]], key="theme_select", label_visibility="collapsed")
        if theme != st.session_state.theme:
            st.session_state.theme = theme
    
    # Refresh settings
    st.caption(texts["refresh_settings"])
    col1, col2 = st.columns([2, 1])
    with col1:
        auto_refresh = st.checkbox(texts["auto_refresh"], value=st.session_state.auto_refresh)
        if auto_refresh != st.session_state.auto_refresh:
            st.session_state.auto_refresh = auto_refresh
    with col2:
        if st.button("🔄", help=texts["manual_refresh"]):
            st.rerun()
    
    # Cryptocurrency selection
    st.caption(texts["select_coin"])
    coins = {
        "BTC": "Bitcoin",
        "ETH": "Ethereum",
        "BNB": "Binance Coin",
        "XRP": "Ripple",
        "ADA": "Cardano",
        "DOGE": "Dogecoin",
        "DOT": "Polkadot",
        "AVAX": "Avalanche",
        "MATIC": "Polygon"
    }
    selected_coin = st.selectbox("", list(coins.keys()), label_visibility="collapsed")
    selected_coin_label = f"{selected_coin}-USDT"
    
    # Timeframe selection
    st.caption(texts["select_timeframe"])
    timeframes = {
        "1m": "1 Minute",
        "5m": "5 Minutes",
        "15m": "15 Minutes",
        "30m": "30 Minutes",
        "1h": "1 Hour",
        "4h": "4 Hours",
        "1d": "1 Day",
        "1w": "1 Week"
    }
    selected_timeframe = st.selectbox("", list(timeframes.keys()), index=5, label_visibility="collapsed")
    selected_timeframe_label = timeframes[selected_timeframe]
    
    # Chart settings
    st.caption(texts["chart_settings"])
    show_grid = st.checkbox(texts["show_grid"], value=st.session_state.show_grid)
    if show_grid != st.session_state.show_grid:
        st.session_state.show_grid = show_grid
    
    show_crosshair = st.checkbox(texts["show_crosshair"], value=st.session_state.show_crosshair)
    if show_crosshair != st.session_state.show_crosshair:
        st.session_state.show_crosshair = show_crosshair
    
    # Indicators settings
    st.sidebar.markdown(f"### {texts['indicators_label']}")
    
    # Moving Average settings
    st.sidebar.markdown("#### Moving Average")
    ma_col1, ma_col2 = st.sidebar.columns([3, 1])
    with ma_col1:
        ma_period = st.number_input("Period", min_value=1, value=20, key="ma_period")
    with ma_col2:
        if st.button("+", key="add_ma"):
            st.session_state.indicators['MA'].append({
                'period': ma_period,
                'color': '#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
            })
    
    # Display active MAs
    for i, ma in enumerate(st.session_state.indicators['MA']):
        ma_col1, ma_col2 = st.sidebar.columns([3, 1])
        with ma_col1:
            st.markdown(f"MA({ma['period']})")
        with ma_col2:
            if st.button("×", key=f"remove_ma_{i}"):
                st.session_state.indicators['MA'].pop(i)
                st.experimental_rerun()
    
    # MACD settings
    st.sidebar.markdown("#### MACD")
    macd_col1, macd_col2, macd_col3, macd_col4 = st.sidebar.columns([2, 2, 2, 1])
    with macd_col1:
        fast_period = st.number_input("Fast", min_value=1, value=12, key="macd_fast")
    with macd_col2:
        slow_period = st.number_input("Slow", min_value=1, value=26, key="macd_slow")
    with macd_col3:
        signal_period = st.number_input("Signal", min_value=1, value=9, key="macd_signal")
    with macd_col4:
        if st.button("+", key="add_macd"):
            st.session_state.indicators['MACD'].append({
                'fast': fast_period,
                'slow': slow_period,
                'signal': signal_period
            })
    
    # Display active MACDs
    for i, macd in enumerate(st.session_state.indicators['MACD']):
        macd_col1, macd_col2 = st.sidebar.columns([3, 1])
        with macd_col1:
            st.markdown(f"MACD({macd['fast']},{macd['slow']},{macd['signal']})")
        with macd_col2:
            if st.button("×", key=f"remove_macd_{i}"):
                st.session_state.indicators['MACD'].pop(i)
                st.experimental_rerun()
    
    # RSI settings
    st.sidebar.markdown("#### RSI")
    rsi_col1, rsi_col2 = st.sidebar.columns([3, 1])
    with rsi_col1:
        rsi_period = st.number_input("Period", min_value=1, value=14, key="rsi_period")
    with rsi_col2:
        if st.button("+", key="add_rsi"):
            st.session_state.indicators['RSI'].append({
                'period': rsi_period,
                'color': '#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
            })
    
    # Display active RSIs
    for i, rsi in enumerate(st.session_state.indicators['RSI']):
        rsi_col1, rsi_col2 = st.sidebar.columns([3, 1])
        with rsi_col1:
            st.markdown(f"RSI({rsi['period']})")
        with rsi_col2:
            if st.button("×", key=f"remove_rsi_{i}"):
                st.session_state.indicators['RSI'].pop(i)
                st.experimental_rerun()
    
    # Ichimoku settings
    st.sidebar.markdown("#### Ichimoku")
    ichi_col1, ichi_col2, ichi_col3, ichi_col4 = st.sidebar.columns([2, 2, 2, 1])
    with ichi_col1:
        tenkan = st.number_input("Tenkan", min_value=1, value=9, key="ichi_tenkan")
    with ichi_col2:
        kijun = st.number_input("Kijun", min_value=1, value=26, key="ichi_kijun")
    with ichi_col3:
        senkou = st.number_input("Senkou", min_value=1, value=52, key="ichi_senkou")
    with ichi_col4:
        if st.button("+", key="add_ichi"):
            st.session_state.indicators['Ichimoku'].append({
                'tenkan': tenkan,
                'kijun': kijun,
                'senkou': senkou
            })
    
    # Display active Ichimoku
    for i, ichi in enumerate(st.session_state.indicators['Ichimoku']):
        ichi_col1, ichi_col2 = st.sidebar.columns([3, 1])
        with ichi_col1:
            st.markdown(f"Ichimoku({ichi['tenkan']},{ichi['kijun']},{ichi['senkou']})")
        with ichi_col2:
            if st.button("×", key=f"remove_ichi_{i}"):
                st.session_state.indicators['Ichimoku'].pop(i)
                st.experimental_rerun()
    
    # Auto-refresh settings
    st.sidebar.markdown(f"### {texts['auto_refresh_label']}")
    auto_refresh = st.sidebar.checkbox(texts["enable_auto_refresh_label"], value=False)
    if auto_refresh:
        refresh_interval = st.sidebar.number_input(
            texts["refresh_interval_label"],
            min_value=1,
            value=5,
            help=texts["refresh_interval_help"]
        )
    
    # Timezone selection moved to the end
    st.caption(texts["timezone"])
    timezone = st.selectbox("", ["UTC", "Asia/Tehran"], key="timezone_select", label_visibility="collapsed")
    if timezone != st.session_state.timezone:
        st.session_state.timezone = timezone

# Fetch and display data
df = fetch_candles(selected_coin_label, selected_timeframe)
if df is not None:
    plot_candlestick(
        df=df,
        indicators=st.session_state.indicators,
        texts=texts,
        language=st.session_state.language,
        theme=st.session_state.theme,
        show_grid=st.session_state.show_grid,
        show_crosshair=st.session_state.show_crosshair,
        symbol=selected_coin_label,
        timeframe=selected_timeframe_label
    )
else:
    st.error(texts["error_no_data"])