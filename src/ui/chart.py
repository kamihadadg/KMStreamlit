import streamlit as st
import plotly.graph_objects as go
from src.indicators.technical import (
    calculate_ma, calculate_macd, calculate_ichimoku,
    calculate_rsi, calculate_volume_profile
)
from src.api.kucoin import fetch_market_info

def plot_candlestick(df, indicators, ma_periods, macd_params, rsi_period, ichimoku_params, texts, language, theme, show_grid, show_crosshair, selected_coin_label, selected_timeframe_label):
    """Plot candlestick chart with selected indicators"""
    if not df.empty and 'close' in df.columns and not df['close'].isna().all():
        current_price = df['close'].iloc[-1]
        market_info = fetch_market_info(selected_coin_label)
        
        # Display info cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="price-card">
                    <div class="metric-label">{texts['current_price']}</div>
                    <div class="metric-value" style="color: #94a3b8">${current_price:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if market_info:
                price_change = float(market_info.get('changeRate', 0)) * 100
                color = "#22c55e" if price_change >= 0 else "#ef4444"
                st.markdown(f"""
                    <div class="price-card">
                        <div class="metric-label">{texts['price_change']}</div>
                        <div class="metric-value" style="color: {color}">{price_change:+.2f}%</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if market_info:
                volume_24h = float(market_info.get('vol24h', 0))
                st.markdown(f"""
                    <div class="price-card">
                        <div class="metric-label">{texts['volume']}</div>
                        <div class="metric-value" style="color: #94a3b8">${volume_24h:,.0f}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col4:
            if market_info:
                market_cap = float(market_info.get('marketCap', 0))
                st.markdown(f"""
                    <div class="price-card">
                        <div class="metric-label">{texts['market_cap']}</div>
                        <div class="metric-value" style="color: #94a3b8">${market_cap:,.0f}</div>
                    </div>
                """, unsafe_allow_html=True)

    # Toolbar
    col1, col2, col3 = st.columns(3)
    with col1:
        zoom_in = st.button(texts["zoom_in"])
    with col2:
        zoom_out = st.button(texts["zoom_out"])
    with col3:
        pan_mode = st.button(texts["pan"])

    fig = go.Figure()
    
    # Candlestick chart
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

    # Moving Averages
    if "MA" in indicators:
        colors = ['#ffeb3b', '#ff9800', '#f44336', '#9c27b0', '#3f51b5']
        for i, (label, period) in enumerate(ma_periods.items()):
            ma_data = calculate_ma(df, period)
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=ma_data,
                line=dict(color=colors[i % len(colors)], width=2),
                name=label
            ))

    # MACD
    if "MACD" in indicators:
        macd, signal, histogram = calculate_macd(df, macd_params["fast"], macd_params["slow"], macd_params["signal"])
        fig.add_trace(go.Scatter(x=df['timestamp'], y=macd, line=dict(color='#26a69a'), name="MACD", yaxis="y2"))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=signal, line=dict(color='#ff9800'), name="Signal" if language == "English" else "سیگنال", yaxis="y2"))
        fig.add_bar(x=df['timestamp'], y=histogram, name="Histogram" if language == "English" else "هیستوگرام", marker_color='gray', yaxis="y2")

    # Ichimoku
    if "Ichimoku" in indicators:
        tenkan, kijun, senkou_a, senkou_b, chikou = calculate_ichimoku(df, ichimoku_params["tenkan"], ichimoku_params["kijun"], ichimoku_params["senkou"])
        fig.add_trace(go.Scatter(x=df['timestamp'], y=tenkan, line=dict(color='#ff0000'), name="Tenkan" if language == "English" else "تنکان"))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=kijun, line=dict(color='#0000ff'), name="Kijun" if language == "English" else "کیجون"))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=senkou_a, line=dict(color='#00ff00'), name="Senkou A" if language == "English" else "سنکو A", fill='tonexty', fillcolor='rgba(0,255,0,0.2)'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=senkou_b, line=dict(color='#ff00ff'), name="Senkou B" if language == "English" else "سنکو B", fill='tonexty', fillcolor='rgba(255,0,255,0.2)'))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=chikou, line=dict(color='#00ffff'), name="Chikou" if language == "English" else "چیکو"))

    # RSI
    if "RSI" in indicators:
        rsi = calculate_rsi(df, rsi_period)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=rsi, line=dict(color='#ab47bc'), name="RSI", yaxis="y3"))

    # Chart settings
    fig.update_layout(
        title=f"{selected_coin_label} {selected_timeframe_label}",
        xaxis_title="",
        yaxis_title=texts["price_label"],
        template="plotly_dark" if theme == texts["dark"] else "plotly_white",
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1h", step="hour", stepmode="backward"),
                    dict(count=6, label="6h", step="hour", stepmode="backward"),
                    dict(count=12, label="12h", step="hour", stepmode="backward"),
                    dict(step="all", label="All" if language == "English" else "همه")
                ]),
                bgcolor="#1e293b" if theme == texts["dark"] else "#ffffff",
                activecolor="#3b82f6"
            ),
            type="date",
            showgrid=show_grid,
            gridcolor="#444" if theme == texts["dark"] else "#ddd"
        ),
        yaxis=dict(
            autorange=True,
            fixedrange=False,
            showgrid=show_grid,
            gridcolor="#444" if theme == texts["dark"] else "#ddd"
        ),
        dragmode="pan" if pan_mode else "zoom",
        hovermode="x unified" if show_crosshair else "closest",
        height=600,
        margin=dict(l=40, r=40, t=80, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor="#0f172a" if theme == texts["dark"] else "#ffffff",
        plot_bgcolor="#0f172a" if theme == texts["dark"] else "#ffffff",
        font=dict(color="#e2e8f0" if theme == texts["dark"] else "#1e293b")
    )

    # Additional axes settings
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

    # Toolbar settings
    fig.update_layout(
        modebar=dict(
            bgcolor="#0f172a" if theme == texts["dark"] else "#ffffff",
            color="#e2e8f0" if theme == texts["dark"] else "#1e293b",
            activecolor="#3b82f6"
        ),
        modebar_add=["v1hovermode", "toggleSpikelines"],
        modebar_remove=["lasso2d", "select2d"]
    )

    # Zoom settings
    if zoom_in:
        fig.update_layout(xaxis_range=[df['timestamp'].iloc[-50], df['timestamp'].iloc[-1]])
    if zoom_out:
        fig.update_layout(xaxis_range=[df['timestamp'].iloc[0], df['timestamp'].iloc[-1]])

    st.plotly_chart(fig, use_container_width=True) 