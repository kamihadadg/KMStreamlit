import streamlit as st
import plotly.graph_objects as go
from src.indicators.technical import (
    calculate_ma, calculate_macd, calculate_ichimoku,
    calculate_rsi, calculate_volume_profile, find_support_resistance
)
from src.api.kucoin import fetch_market_info
import time

def plot_candlestick(df, indicators, texts, language, theme, show_grid, show_crosshair, 
                   symbol, timeframe):
    # Display market info
    market_info = fetch_market_info(symbol)
    if market_info:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{texts["price_label"]}</div>
                    <div class="info-value price-value">${float(market_info['last']):,.3f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            change_value = float(market_info['changeRate'])*100
            change_class = "change-value-up" if change_value > 0 else "change-value-down"
            st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{texts["change_label"]}</div>
                    <div class="info-value {change_class}">{change_value:+.3f}%</div>
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
        for ma in indicators['MA']:
            ma_data = df['close'].rolling(window=ma['period']).mean()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=ma_data,
                line=dict(color=ma['color'], width=1),
                name=f"MA({ma['period']})"
            ))
        
        # Add MACD
        for macd_config in indicators['MACD']:
            exp1 = df['close'].ewm(span=macd_config['fast'], adjust=False).mean()
            exp2 = df['close'].ewm(span=macd_config['slow'], adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=macd_config['signal'], adjust=False).mean()
            histogram = macd - signal
            
            # Create new y-axis for MACD
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=macd,
                name=f"MACD({macd_config['fast']},{macd_config['slow']},{macd_config['signal']})",
                line=dict(color='#3b82f6', width=1),
                yaxis='y2'
            ))
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=signal,
                name='Signal',
                line=dict(color='#f59e0b', width=1),
                yaxis='y2'
            ))
            
            fig.add_trace(go.Bar(
                x=df['timestamp'],
                y=histogram,
                name='Histogram',
                marker=dict(
                    color=['#22c55e' if val >= 0 else '#ef4444' for val in histogram],
                    opacity=0.5
                ),
                yaxis='y2'
            ))
        
        # Add RSI
        for rsi_config in indicators['RSI']:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=rsi_config['period']).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_config['period']).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=rsi,
                name=f"RSI({rsi_config['period']})",
                line=dict(color=rsi_config['color'], width=1),
                yaxis='y3'
            ))
        
        # Add Ichimoku
        for ichi_config in indicators['Ichimoku']:
            # Conversion Line (Tenkan-sen)
            high_9 = df['high'].rolling(window=ichi_config['tenkan']).max()
            low_9 = df['low'].rolling(window=ichi_config['tenkan']).min()
            tenkan_sen = (high_9 + low_9) / 2
            
            # Base Line (Kijun-sen)
            high_26 = df['high'].rolling(window=ichi_config['kijun']).max()
            low_26 = df['low'].rolling(window=ichi_config['kijun']).min()
            kijun_sen = (high_26 + low_26) / 2
            
            # Leading Span A (Senkou Span A)
            senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(ichi_config['kijun'])
            
            # Leading Span B (Senkou Span B)
            high_52 = df['high'].rolling(window=ichi_config['senkou']).max()
            low_52 = df['low'].rolling(window=ichi_config['senkou']).min()
            senkou_span_b = ((high_52 + low_52) / 2).shift(ichi_config['kijun'])
            
            # Lagging Span (Chikou Span)
            chikou_span = df['close'].shift(-ichi_config['kijun'])
            
            # Add traces
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=tenkan_sen,
                name=f'Tenkan-sen ({ichi_config["tenkan"]})',
                line=dict(color='#3b82f6', width=1)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=kijun_sen,
                name=f'Kijun-sen ({ichi_config["kijun"]})',
                line=dict(color='#ef4444', width=1)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=senkou_span_a,
                name=f'Senkou Span A',
                line=dict(color='#22c55e', width=1),
                fill=None
            ))
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=senkou_span_b,
                name=f'Senkou Span B',
                line=dict(color='#ef4444', width=1),
                fill='tonexty'
            ))
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=chikou_span,
                name=f'Chikou Span',
                line=dict(color='#8b5cf6', width=1)
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
            # Skip levels with strength 11
            if strength == 11:
                continue
                
            # Only show support lines below current price
            if price < current_price:
                fig.add_hline(y=price, line_dash="dash", line_color="#22c55e", 
                             line_width=0.5)
        
        for price, _, strength in resistance_levels:
            # Skip levels with strength 11
            if strength == 11:
                continue
                
            # Only show resistance lines above current price
            if price > current_price:
                fig.add_hline(y=price, line_dash="dash", line_color="#ef4444", 
                             line_width=0.5)
        
        # Update layout for multiple y-axes
        layout_updates = {
            'yaxis': dict(
                title='Price',
                side='right',
                showgrid=show_grid
            ),
            'xaxis': dict(
                title='Time',
                showgrid=show_grid
            ),
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': dict(color='#e2e8f0'),
            'margin': dict(t=30, l=0, r=0, b=0),
            'showlegend': True,
            'legend': dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(0,0,0,0)'
            )
        }
        
        # Add MACD subplot if exists
        if indicators['MACD']:
            layout_updates['yaxis2'] = dict(
                title='MACD',
                overlaying='y',
                side='right',
                showgrid=show_grid,
                anchor='free',
                position=1
            )
        
        # Add RSI subplot if exists
        if indicators['RSI']:
            layout_updates['yaxis3'] = dict(
                title='RSI',
                overlaying='y',
                side='right',
                range=[0, 100],
                showgrid=show_grid,
                anchor='free',
                position=0.95
            )
        
        # Update layout
        fig.update_layout(**layout_updates)
        
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
            <div class="sidebar-section">
                <h3>Support & Resistance Levels</h3>
                <div class="level-section">

        """, unsafe_allow_html=True)
        
        # Display resistance levels above current price
       
        st.markdown("""
                    </ul>
                </div>
                <div class="level-section">
                    <h4>Resistance Levels</h4>
                    <ul class="level-list">
        """, unsafe_allow_html=True)
       
       
        for price, _, strength in resistance_levels:
            if strength == 11:  # Skip levels with strength 11
                continue
            if price > current_price:
                st.markdown(f"""
                    <li class="level-item">
                        <span class="level-price resistance">${price:,.3f}</span>
                       
                    </li>
                """, unsafe_allow_html=True)
        
        st.markdown("""
                    </ul>
                </div>
                <div class="level-section">
                    <h4>Support Levels</h4>
                    <ul class="level-list">
        """, unsafe_allow_html=True)
        
        # Display support levels below current price
        for price, _, strength in support_levels:
            if strength == 11:  # Skip levels with strength 11
                continue
            if price < current_price:
                st.markdown(f"""
                    <li class="level-item">
                        <span class="level-price support">${price:,.3f}</span>
                        
                    </li>
                """, unsafe_allow_html=True)
        
        st.markdown("""
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True) 