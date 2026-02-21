import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import resend

# 1. API Setup
resend.api_key = "re_Kt1sqzZ4_3N9hxXX1mCEkvRMyEZuhZS83"

st.set_page_config(page_title="AAPL Alpha Alerter", page_icon="📈")
st.title("🍎 AAPL Automated Stock Alerter")

# 2. Function to send the email
def send_email_alert(ticker, current_price, change_percent):
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "YOUR_EMAIL_HERE@gmail.com", # <--- DOUBLE CHECK THIS IS YOUR EMAIL
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

    # 4. Display Metrics
    col1, col2 = st.columns(2)
    col1.metric("Current Price", f"${current_price:.2f}")
    col2.metric("Daily Change", f"{change_percent:.2%}", delta=f"{change_percent:.2%}")

    # --- 5. THE CHART (The missing piece!) ---
    st.subheader("Price Trend (Past 30 Days)")
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Pick color based on performance
    line_color = 'green' if change_percent > 0 else 'red'
    
    ax.plot(data.index, data['Close'], color=line_color, linewidth=2)
    ax.fill_between(data.index, data['Close'], alpha=0.1, color=line_color) # Adds a nice shading
    ax.set_ylabel("Price ($)")
    plt.xticks(rotation=45)
    
    st.pyplot(fig) 
    # ------------------------------------------

    # 6. The Logic Trigger
    if st.button('Run Manual Scan & Test Email'):
        if abs(change_percent) > 0.02:
            st.warning(f"Significant movement ({change_percent:.2%}). Sending email...")
            send_email_alert(ticker, current_price, change_percent)
        else:
            st.info(f"Movement is {change_percent:.2%}. Threshold for email is 2%.")
else:
    st.error("Waiting for market data...")
