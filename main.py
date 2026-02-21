import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def check_stock():
    ticker = "AAPL"
    data = yf.Ticker(ticker).history(period="3mo")

    data["Return"] = data["Close"].pct_change()
    latest = data.iloc[-1]

    price_change = latest["Return"]
    price_shift = abs(price_change) > 0.02

    avg_volume = data["Volume"].rolling(20).mean().iloc[-1]
    volume_spike = latest["Volume"] > 1.5 * avg_volume

    # Update GUI labels
    price_label.config(text=f"Price: ${latest['Close']:.2f}")
    change_label.config(text=f"Change: {price_change:.2%}")
    volume_label.config(text=f"Volume: {latest['Volume']:.0f}")

    if price_shift or volume_spike:
        status_label.config(text="ALERT: Market Movement Detected", fg="red")
        message = f"Price: {price_change:.2%} | Volume: {latest['Volume']:.0f}"
        mac_notification("Stock Alert: AAPL", message)
    else:
        status_label.config(text="Market Normal", fg="green")

    # Update mini chart
    plot_data = data["Close"].tail(30)  # last 30 days
    ax.clear()
    ax.plot(plot_data.index, plot_data.values)
    ax.set_title("AAPL - Last 30 Days Close Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.tick_params(axis='x', rotation=45)

    fig.tight_layout()
    canvas.draw()

# Streamlit Web Interface 
st.title("AAPL Stock Alert Bot")

# buttons and texts on the website
if st.button('Check Now'):
    # This runs the logic and displays the result
    st.write("Fetching latest data...")
    
    # Simple display metrics
    col1, col2 = st.columns(2)
    col1.metric("Price", f"${data['Close'].iloc[-1]:.2f}")
    col2.metric("Volume", f"{data['Volume'].iloc[-1]:,}")
    
    # Display the chart
    st.pyplot(fig)
else:
    st.write("Click the button to refresh data.")
    
# Mini chart setup
fig = Figure(figsize=(7, 3.5), dpi=100)
ax = fig.add_subplot(111)

st.pyplot(fig)

# data and chart code 

# tells the website to display the chart
st.pyplot(fig)

# Values to make we got the numbers 
current_price = data['Close'].values[-1]
st.write(f"The current price of AAPL is: ${current_price:.2f}")
