import streamlit as st
import pandas as pd
from src.config.settings import setup_page_config, get_styles
from src.config.texts import get_texts
from src.api.kucoin import fetch_candles
from src.ui.chart import plot_candlestick

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

# Get texts based on language
texts = get_texts(st.session_state.language)

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
    
    # Indicators with reduced spacing
    st.caption(texts["indicators"])
    indicators = []
    
    # Moving Averages
    if st.checkbox(texts["ma"]):
        indicators.append("MA")
        st.caption(texts["ma_settings"])
        ma_periods = {}
        for i in range(1, 6):
            default_value = 20 if i == 1 else 50 if i == 2 else 100 if i == 3 else 200 if i == 4 else 20
            period = st.number_input(f"{texts['ma_period']} {i}", min_value=1, max_value=200, value=default_value)
            if period > 0:
                ma_periods[f"MA{period}"] = period
    else:
        ma_periods = {}
    
    # MACD
    if st.checkbox(texts["macd"]):
        indicators.append("MACD")
        st.caption(texts["macd_settings"])
        macd_params = {
            "fast": st.number_input(texts["macd_fast"], min_value=1, max_value=100, value=12),
            "slow": st.number_input(texts["macd_slow"], min_value=1, max_value=100, value=26),
            "signal": st.number_input(texts["macd_signal"], min_value=1, max_value=100, value=9)
        }
    else:
        macd_params = {"fast": 12, "slow": 26, "signal": 9}
    
    # RSI
    if st.checkbox(texts["rsi"]):
        indicators.append("RSI")
        st.caption(texts["rsi_settings"])
        rsi_period = st.number_input(texts["rsi_period"], min_value=1, max_value=100, value=14)
    else:
        rsi_period = 14
    
    # Ichimoku
    if st.checkbox(texts["ichimoku"]):
        indicators.append("Ichimoku")
        st.caption(texts["ichimoku_settings"])
        ichimoku_params = {
            "tenkan": st.number_input(texts["ichimoku_tenkan"], min_value=1, max_value=100, value=9),
            "kijun": st.number_input(texts["ichimoku_kijun"], min_value=1, max_value=100, value=26),
            "senkou": st.number_input(texts["ichimoku_senkou"], min_value=1, max_value=100, value=52)
        }
    else:
        ichimoku_params = {"tenkan": 9, "kijun": 26, "senkou": 52}
    
    # Timezone selection moved to the end
    st.caption(texts["timezone"])
    timezone = st.selectbox("", ["UTC", "Asia/Tehran"], key="timezone_select", label_visibility="collapsed")
    if timezone != st.session_state.timezone:
        st.session_state.timezone = timezone

# Main content
# st.title(texts["title"])
# st.markdown(texts["subtitle"])

# Fetch and display data
df = fetch_candles(selected_coin_label, selected_timeframe)
if not df.empty:
    # Convert MA periods to list of integers
    ma_periods_list = [int(period) for period in ma_periods.values()]
    
    plot_candlestick(
        df, indicators, ma_periods_list, macd_params, rsi_period,
        ichimoku_params, texts, st.session_state.language,
        st.session_state.theme, st.session_state.show_grid,
        st.session_state.show_crosshair, selected_coin_label,
        selected_timeframe_label
    )
else:
    st.error(texts["error_no_data"])