import streamlit as st
import plotly.graph_objects as go
from src.indicators.technical import (
    calculate_ma, calculate_macd, calculate_ichimoku,
    calculate_rsi, calculate_volume_profile, find_support_resistance
)
from src.api.kucoin import fetch_market_info

def plot_candlestick(df, indicators, ma_periods, macd_params, rsi_period,
                    ichimoku_params, texts, language, theme, show_grid,
                    show_crosshair, symbol, timeframe):
    """Plot candlestick chart with selected indicators"""
    # Display market info
    market_info = fetch_market_info(symbol)
    if market_info:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{texts["current_price"]}</div>
                    <div class="info-value">${float(market_info['last']):,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            change_color = "#22c55e" if float(market_info['changeRate']) > 0 else "#ef4444"
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{texts["price_change"]}</div>
                    <div class="info-value" style="color: {change_color}">
                        {float(market_info['changeRate'])*100:+.2f}%
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{texts["volume"]}</div>
                    <div class="info-value">${float(market_info['volValue']):,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{texts["market_cap"]}</div>
                    <div class="info-value">${float(market_info['vol']):,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Chart controls
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button(texts["zoom_in"]):
            st.session_state.zoom_level = min(st.session_state.get('zoom_level', 1) + 0.1, 2)
    with col2:
        if st.button(texts["zoom_out"]):
            st.session_state.zoom_level = max(st.session_state.get('zoom_level', 1) - 0.1, 0.5)
    with col3:
        if st.button(texts["update"]):
            st.experimental_rerun()
    
    # Create candlestick chart
    fig = go.Figure()
    
    # Add candlestick
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='#22c55e',
        decreasing_line_color='#ef4444',
        increasing_fillcolor='#22c55e',
        decreasing_fillcolor='#ef4444',
        name='OHLC'
    ))
    
    # Add Moving Averages
    if "MA" in indicators:
        colors = ['#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#10b981']
        for i, period in enumerate(ma_periods):
            ma = calculate_ma(df, period)
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=ma,
                name=f'MA{period}',
                line=dict(color=colors[i % len(colors)], width=2)
            ))
    
    # Add MACD
    if "MACD" in indicators:
        macd, signal, hist = calculate_macd(df, macd_params["fast"], macd_params["slow"], macd_params["signal"])
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=macd,
            name='MACD',
            line=dict(color='#3b82f6', width=2),
            yaxis='y2'
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=signal,
            name='Signal',
            line=dict(color='#f59e0b', width=2),
            yaxis='y2'
        ))
        fig.add_trace(go.Bar(
            x=df['timestamp'],
            y=hist,
            name='Histogram',
            marker_color='#22c55e' if hist[-1] > 0 else '#ef4444',
            yaxis='y2'
        ))
    
    # Add Ichimoku Cloud
    if "Ichimoku" in indicators:
        tenkan, kijun, senkou_span_a, senkou_span_b = calculate_ichimoku(
            df, ichimoku_params["tenkan"], ichimoku_params["kijun"], ichimoku_params["senkou"]
        )
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=tenkan,
            name='Tenkan',
            line=dict(color='#3b82f6', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=kijun,
            name='Kijun',
            line=dict(color='#f59e0b', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=senkou_span_a,
            name='Senkou Span A',
            line=dict(color='#22c55e', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=senkou_span_b,
            name='Senkou Span B',
            line=dict(color='#ef4444', width=2)
        ))
    
    # Add RSI
    if "RSI" in indicators:
        rsi = calculate_rsi(df, rsi_period)
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=rsi,
            name='RSI',
            line=dict(color='#8b5cf6', width=2),
            yaxis='y3'
        ))
    
    # Add Support and Resistance Levels
    support_levels, resistance_levels = find_support_resistance(df)
    
    # Display support and resistance levels
    st.markdown(f"### {texts['support_levels']} & {texts['resistance_levels']}")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {texts['support_levels']}")
        for price, _, strength in support_levels:
            st.markdown(f"- ${price:,.2f} ({texts['strength']}: {strength})")
            fig.add_hline(y=price, line_dash="dash", line_color="#22c55e", 
                         annotation_text=f"{texts['support_levels']}: ${price:,.2f}", 
                         annotation_position="right")
    
    with col2:
        st.markdown(f"#### {texts['resistance_levels']}")
        for price, _, strength in resistance_levels:
            st.markdown(f"- ${price:,.2f} ({texts['strength']}: {strength})")
            fig.add_hline(y=price, line_dash="dash", line_color="#ef4444", 
                         annotation_text=f"{texts['resistance_levels']}: ${price:,.2f}", 
                         annotation_position="right")
    
    # Update layout
    fig.update_layout(
        title=f"{symbol} - {timeframe}",
        yaxis_title="Price",
        xaxis_title="Time",
        template="plotly_dark" if theme == texts["dark"] else "plotly_white",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        xaxis=dict(
            rangeslider=dict(visible=False),
            gridcolor='rgba(128, 128, 128, 0.2)' if show_grid else 'rgba(0, 0, 0, 0)',
            showgrid=show_grid
        ),
        yaxis=dict(
            gridcolor='rgba(128, 128, 128, 0.2)' if show_grid else 'rgba(0, 0, 0, 0)',
            showgrid=show_grid
        ),
        hovermode='x unified' if show_crosshair else False,
        height=600,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="#0f172a" if theme == texts["dark"] else "#ffffff",
        plot_bgcolor="#0f172a" if theme == texts["dark"] else "#ffffff",
        font=dict(color="#e2e8f0" if theme == texts["dark"] else "#1e293b")
    )
    
    # Add secondary y-axis for MACD and RSI
    if "MACD" in indicators:
        fig.update_layout(
            yaxis2=dict(
                title="MACD",
                overlaying="y",
                side="right",
                position=0.95,
                gridcolor='rgba(128, 128, 128, 0.2)' if show_grid else 'rgba(0, 0, 0, 0)',
                showgrid=show_grid
            )
        )
    
    if "RSI" in indicators:
        fig.update_layout(
            yaxis3=dict(
                title="RSI",
                overlaying="y",
                side="right",
                position=0.85,
                gridcolor='rgba(128, 128, 128, 0.2)' if show_grid else 'rgba(0, 0, 0, 0)',
                showgrid=show_grid,
                range=[0, 100]
            )
        )
    
    # Configure toolbar
    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'modeBarButtonsToAdd': ['drawline', 'eraseshape']
    }
    
    # Apply zoom level
    zoom_level = st.session_state.get('zoom_level', 1)
    fig.update_layout(
        yaxis=dict(
            range=[
                df['low'].min() * (1 - (zoom_level - 1) * 0.1),
                df['high'].max() * (1 + (zoom_level - 1) * 0.1)
            ]
        )
    )
    
    # Display chart
    st.plotly_chart(fig, use_container_width=True, config=config) 