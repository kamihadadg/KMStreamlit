# Technical Chart

A powerful technical analysis chart built with Streamlit and Plotly, featuring:

- Real-time cryptocurrency price data from KuCoin
- Multiple technical indicators:
  - Moving Averages (MA) with customizable periods and colors
  - MACD (Moving Average Convergence Divergence)
  - RSI (Relative Strength Index)
  - Ichimoku Cloud
- Support and Resistance level detection
- Market information display (Price, 24h Change, Volume, Market Cap)
- Auto-refresh functionality
- Dark/Light theme support
- Multiple language support (English, Persian, German)
- Grid and crosshair display options
- Multiple timeframe options (1m to 1w)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kamihadadg/KMStreamlit.git
cd technical-chart
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser. Use the sidebar to:

- Select your preferred language
- Choose dark/light theme
- Select cryptocurrency pair
- Choose timeframe
- Toggle grid and crosshair
- Add/remove technical indicators
- Enable auto-refresh

## Features

### Market Information
- Current price
- 24-hour price change (with color coding)
- 24-hour trading volume
- Market capitalization

### Technical Indicators
- Moving Averages (MA)
  - Add multiple MAs with different periods
  - Customize colors
  - Remove individual MAs
- MACD
  - Customizable fast, slow, and signal periods
  - Histogram with color coding
  - Multiple MACD indicators
- RSI
  - Adjustable period
  - Multiple RSI indicators
  - Custom colors
- Ichimoku Cloud
  - Customizable Tenkan-sen, Kijun-sen, and Senkou Span periods
  - Multiple Ichimoku indicators

### Support and Resistance
- Automatic detection of support and resistance levels
- Strength-based filtering
- Color coding (green for support, red for resistance)
- Display only relevant levels based on current price

### Chart Settings
- Dark/Light theme
- Grid display toggle
- Crosshair toggle
- Multiple timeframe options
- Auto-refresh with customizable interval

### Multilingual Support
- English
- Persian (فارسی)
- German (Deutsch)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 