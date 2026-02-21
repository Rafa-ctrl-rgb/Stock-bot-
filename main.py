import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import resend

# 1. API Setup
resend.api_key = "re_Kt1sqzZ4_3N9hxXX1mCEkvRMyEZuhZS83"

st.set_page_config(page_title="AAPL Alpha Alerter", page_icon="📈", layout="centered")

# Custom CSS to make the Streamlit background dark to match the chart
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    </style>
    """, unsafe_allow_texts=True)

st.title("🍎 AAPL Automated Stock Alerter")

# 2. Function to send the email
def send_email_alert(ticker, current_price, change_percent):
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "YOUR_EMAIL_HERE@gmail.com", # <--- CHANGE THIS
            "subject": f"🚨 {ticker} Movement Alert: {change_percent:.2%}",
            "html": f"<h3>Stock Alert</h3><p>{ticker} moved {change_percent:.2%}. Price: ${current_price:.2f}</p>"
        })
        st.success("📩 Alert email sent!")
    except Exception as e:
        st.error(f"Email failed: {e}")

# 3. Data Fetching
ticker = "AAPL"
data = yf.download(ticker, period="1mo", interval="1d")

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

if not data.empty and len(data) >= 2:
    current_price = float(data["Close"].iloc[-1])
    yesterday_price = float(data["Close"].iloc[-2])
    change_percent = (current_price - yesterday_price) / yesterday_price

    # 4. Metrics
    col1, col2 = st.columns(2)
    col1.metric("Current Price", f"${current_price:.2f}")
    col2.metric("Daily Change", f"{change_percent:.2%}", delta=f"{change_percent:.2%}")

    # --- 5. THE FANCY DARK CHART ---
    st.subheader("Price Trend (Past 30 Days)")
    
    # Set the dark theme
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Choose color: Electric Green or Neon Red
    color = '#00ff88' if change_percent > 0 else '#ff4b4b'
    
    # Plot the line with a slight glow
    ax.plot(data.index, data['Close'], color=color, linewidth=2.5, alpha=0.9)
    
    # Add a gradient-style area fill
    ax.fill_between(data.index, data['Close'], min(data['Close
