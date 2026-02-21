import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(page_title="AAPL Stock Alert Bot", layout="centered")

st.title("🍎 AAPL Stock Alert Bot")
st.write("Real-time market analysis and volatility detection.")

# 2. Fetch Data
ticker = "AAPL"
# We fetch 3 months of data to calculate the 20-day average volume
data = yf.download(ticker, period="3mo", interval="1d")

# FIX: This line flattens the yfinance data so it's simple to read
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

if not data.empty:
    # 3. Calculations (Using .iloc[-1] to get the single most recent value)
    data["Return"] = data["Close"].pct_change()
    
    # We use .item() to ensure we get a single number, not a list
    current_price = float(data["Close"].iloc[-1])
    price_change = float(data["Return"].iloc[-1])
    current_volume = float(data["Volume"].iloc[-1])
    
    # Volatility Logic
    price_shift = abs(price_change) > 0.02
    
    avg_volume = data["Volume"].rolling(20).mean().iloc[-1]
    volume_spike = current_volume > (1.5 * avg_volume)

    # 4. Interactive UI
    if st.button('Check Now'):
        st.balloons()
        
        # This 'if' will now work because price_shift is a single True/False
        if price_shift or volume_spike:
            st.error("⚠️ ALERT: Market Movement Detected")
            if price_shift: st.write("- Significant price move (> 2%)")
            if volume_spike: st.write("- Unusual volume spike detected")
        else:
            st.success("✅ Market Status: Normal")

        # 5. Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Price", f"${current_price:.2f}")
        col2.metric("Change", f"{price_change:.2%}")
        col3.metric("Volume", f"{current_volume:,.0f}")

        # 6. Charting
        st.subheader("30-Day Trend")
        plot_data = data["Close"].tail(30)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(plot_data.index, plot_data.values, color='#007bff', linewidth=2)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("Click the button to scan for alerts.")
else:
    st.error("Data fetch failed. Check your internet or ticker symbol.")
