import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(page_title="AAPL Stock Alert Bot", layout="centered")

st.title("🍎 AAPL Stock Alert Bot")
st.write("Real-time market analysis and volatility detection.")

# 2. Data Fetching Logic
ticker = "AAPL"

# We fetch the data at the start so the app has something to show immediately
data = yf.download(ticker, period="3mo", interval="1d")

if not data.empty:
    # 3. Calculations
    data["Return"] = data["Close"].pct_change()
    latest = data.iloc[-1]
    
    # Calculate price change and volume spikes
    price_change = latest["Return"]
    price_shift = abs(price_change) > 0.02
    
    avg_volume = data["Volume"].rolling(20).mean().iloc[-1]
    volume_spike = latest["Volume"] > 1.5 * avg_volume

    # 4. Interactive UI: The "Check Now" Button
    if st.button('Check Now'):
        st.balloons() # Added a little flair for your presentation!
        
        # Display Status Alert
        if price_shift or volume_spike:
            st.error("⚠️ ALERT: Market Movement Detected")
        else:
            st.success("✅ Market Status: Normal")

        # 5. Metric Layout (Side-by-Side)
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${latest['Close']:.2f}")
        col2.metric("Daily Change", f"{price_change:.2%}")
        col3.metric("Volume", f"{latest['Volume']:,}")

        # 6. Charting Logic
        st.subheader("Last 30 Days Performance")
        plot_data = data["Close"].tail(30)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(plot_data.index, plot_data.values, color='#007bff', linewidth=2)
        ax.set_ylabel("Price ($)")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        
        # Display the chart on the website
        st.pyplot(fig)
        
    else:
        st.info("Click the 'Check Now' button to run the latest analysis.")
        
else:
    st.error("Failed to retrieve data. Please refresh the page.")

# 7. Footer Price Update
if not data.empty:
    st.divider()
    current_price = data['Close'].iloc[-1]
    st.caption(f"Last heartbeat check for {ticker}: ${current_price:.2f}")
