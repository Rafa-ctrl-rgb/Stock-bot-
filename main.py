import streamlit as st
import yfinance as yf
import pandas as pd
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
            "to": "28rafaelg@his.ac.zw", 
            "subject": f"🚨 {ticker} Movement Alert: {change_percent:.2%}",
            "html": f"""
                <h3>Stock Alert Triggered</h3>
                <p><strong>Ticker:</strong> {ticker}</p>
                <p><strong>Current Price:</strong> ${current_price:.2f}</p>
                <p><strong>Daily Change:</strong> {change_percent:.2%}</p>
                <p>This alert was generated because the stock moved more than 2%.</p>
            """
        })
        st.success("📩 Alert email sent to your inbox!")
    except Exception as e:
        st.error(f"Email failed to send: {e}")

# 3. Data Fetching
ticker = "AAPL"
data = yf.download(ticker, period="2d", interval="1d")

# Clean up data headers
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

if not data.empty and len(data) >= 2:
    # Get prices
    current_price = float(data["Close"].iloc[-1])
    yesterday_price = float(data["Close"].iloc[-2])
    change_percent = (current_price - yesterday_price) / yesterday_price

    # 4. Display Dashboard
    col1, col2 = st.columns(2)
    col1.metric("Current Price", f"${current_price:.2f}")
    col2.metric("Daily Change", f"{change_percent:.2%}", delta=f"{change_percent:.2%}")

    # 5. The Logic Trigger
    if st.button('Run Manual Scan'):
        if abs(change_percent) > 0.02:
            st.warning(f"Movement is {change_percent:.2%}. Sending email...")
            send_email_alert(ticker, current_price, change_percent)
        else:
            st.info(f"Movement is only {change_percent:.2%}. No email sent.")
else:
    st.error("Waiting for market data...")
