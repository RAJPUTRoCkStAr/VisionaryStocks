import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import time
from streamlit_lottie import st_lottie
from lotti import lottie_report  

def fetch_stock_data(ticker, period="1d", interval="1m"):
    return yf.Ticker(ticker).history(period=period, interval=interval)

def plot_chart(data, chart_type, ticker):
    if chart_type == "Line Chart":
        fig = go.Figure(go.Scatter(
            x=data.index, 
            y=data['Close'], 
            mode='lines', 
            name='Close Price'
        ))
        fig.update_layout(title=f"{ticker} - Line Chart", xaxis_title="Time", yaxis_title="Price")

    elif chart_type == "Candlestick Chart":
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            increasing_line_color='green',
            decreasing_line_color='red'
        )])
        fig.update_layout(title=f"{ticker} - Candlestick Chart", xaxis_title="Time", yaxis_title="Price")

    elif chart_type == "Bar Chart":
        fig = go.Figure(go.Bar(
            x=data.index, 
            y=data['Close'], 
            name='Close Price'
        ))
        fig.update_layout(title=f"{ticker} - Bar Chart", xaxis_title="Time", yaxis_title="Price")

    elif chart_type == "OHLC Chart":
        fig = go.Figure(data=[go.Ohlc(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            increasing_line_color='green',
            decreasing_line_color='red'
        )])
        fig.update_layout(title=f"{ticker} - OHLC Chart", xaxis_title="Time", yaxis_title="Price")

    return fig

def update_data_and_plot(ticker, chart_placeholder, table_placeholder):
    period, interval = "1d", "1m"
    data = fetch_stock_data(ticker, period, interval)

    if not data.empty:
        if 'Dividends' in data.columns:
            data = data.drop(columns=['Dividends'])
        if 'Stock Splits' in data.columns:
            data = data.drop(columns=['Stock Splits'])

        fig = plot_chart(data, st.session_state.chart_type, ticker)
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        table_placeholder.dataframe(data, use_container_width=True)

def live():
    if 'chart_type' not in st.session_state:
        st.session_state.chart_type = 'Line Chart'

    col11, col12 = st.columns(2)
    with col11:
        st.markdown(f"<h2 style='text-align: left;color:#ff4b4b;'>Real-Time Stock Price Visualization</h2>", unsafe_allow_html=True)
        st.write("In the digital realm of financial markets, real-time data streams provide a window into the ever-changing landscape of stock prices. Amidst the flow of information, an individual embarks on a journey to navigate the complexities of market dynamics. Fueled by a desire for insight, they harness the power of technology to visualize trends and patterns. Through the interplay of candlestick charts and moving averages, they seek to uncover the underlying rhythms of market behavior. As the data unfolds, each fluctuation becomes a thread in the tapestry of market sentiment. In this quest for understanding, they embrace the challenge of deciphering signals amidst the noise. And in the dance between data and interpretation, they find both the exhilaration of discovery and the humbling reminder of the unpredictable nature of markets.")
    with col12:
        st_lottie(lottie_report, speed=1, reverse=True, loop=True, quality='medium', height=None, width=None, key=None)



    option = st.text_input('Enter a Stock Symbol', value='SPY').upper()
    chart_type = st.selectbox("Select chart type:", ["Line Chart", "Candlestick Chart", "Bar Chart", "OHLC Chart"])
    st.session_state.chart_type = chart_type

    chart_placeholder = st.empty()
    table_placeholder = st.empty()

    if st.button('Fetch Live Data'):
        while True:
            if option and st.session_state.chart_type:
                update_data_and_plot(option, chart_placeholder, table_placeholder)
            time.sleep(60)  
            st.rerun()  


