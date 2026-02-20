import streamlit as st
import yfinance as yf
import pandas as pd
import subprocess
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mac_notification(title, text):
    subprocess.call([
        "osascript", "-e",
        f'display notification "{text}" with title "{title}"'
    ])

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

# GUI setup
root = tk.Tk()
root.title("AAPL Stock Alert Bot")

price_label = tk.Label(root, text="Price: --")
price_label.pack()

change_label = tk.Label(root, text="Change: --")
change_label.pack()

volume_label = tk.Label(root, text="Volume: --")
volume_label.pack()

status_label = tk.Label(root, text="Status: --")
status_label.pack()

check_button = tk.Button(root, text="Check Now", command=check_stock)
check_button.pack()

# Mini chart setup
fig = Figure(figsize=(7, 3.5), dpi=100)
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()

