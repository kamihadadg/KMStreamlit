import streamlit as st
import plotly.graph_objects as go
from src.indicators.technical import (
    calculate_ma, calculate_macd, calculate_ichimoku,
    calculate_rsi, calculate_volume_profile, find_support_resistance
)
from src.api.kucoin import fetch_market_info
import time

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
                    <div class="info-label">{texts["price_label"]}</div>
                    <div class="info-value price-value">${float(market_info['last']):,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            change_value = float(market_info['changeRate'])*100
            change_class = "change-value-up" if change_value > 0 else "change-value-down"
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{texts["change_label"]}</div>
                    <div class="info-value {change_class}">{change_value:+.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{texts["volume_label"]}</div>
                    <div class="info-value volume-value">${float(market_info['volValue']):,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{texts["market_cap_label"]}</div>
                    <div class="info-value market-cap-value">${float(market_info['vol']):,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Add spacing between info boxes and chart
        st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    
    # Create two columns for chart and right sidebar
    chart_col, right_sidebar = st.columns([3, 1])
    
    with chart_col:
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
        
        # Get current price
        current_price = float(market_info['last'])
        
        # Sort levels by price (high to low)
        resistance_levels = sorted(resistance_levels, key=lambda x: (-x[0], -x[2]))  # Sort by price desc, then strength desc
        support_levels = sorted(support_levels, key=lambda x: (-x[0], -x[2]))  # Sort by price desc, then strength desc
        
        # Add support and resistance lines to chart
        for price, _, strength in support_levels:
            # Only show support lines below current price
            if price < current_price:
                fig.add_hline(y=price, line_dash="dash", line_color="#22c55e", 
                             line_width=1,
                             annotation_text=f"S: ${price:,.2f}", 
                             annotation_position="right")
        
        for price, _, strength in resistance_levels:
            # Only show resistance lines above current price
            if price > current_price:
                fig.add_hline(y=price, line_dash="dash", line_color="#ef4444", 
                             line_width=1,
                             annotation_text=f"R: ${price:,.2f}", 
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
        
        # Display chart
        st.plotly_chart(fig, use_container_width=True, config=config)
    
    # Display support and resistance levels in right sidebar
    with right_sidebar:
        st.markdown("""
            <div class="right-sidebar">
                <h3>Support & Resistance</h3>
                <h4>Resistance Levels</h4>
                <ul class="level-list">
        """, unsafe_allow_html=True)
        
        # Display resistance levels above current price
        for price, _, strength in resistance_levels:
            if price > current_price and strength != 11:
                st.markdown(f"""
                    <li>
                        <span class="resistance-level">${price:,.2f}</span>
                        <span class="level-strength">{strength}</span>
                    </li>
                """, unsafe_allow_html=True)
        
        st.markdown("""
                </ul>
                <h4>Support Levels</h4>
                <ul class="level-list">
        """, unsafe_allow_html=True)
        
        # Display support levels below current price
        for price, _, strength in support_levels:
            if price < current_price and strength != 11:
                st.markdown(f"""
                    <li>
                        <span class="support-level">${price:,.2f}</span>
                        <span class="level-strength">{strength}</span>
                    </li>
                """, unsafe_allow_html=True)
        
        st.markdown("""
                </ul>
            </div>
        """, unsafe_allow_html=True) 