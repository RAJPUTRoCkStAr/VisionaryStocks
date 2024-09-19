import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
from statsmodels.tsa.ar_model import AutoReg
from streamlit_lottie import st_lottie
from lotti import lottie_predaccu

def fetch_historical_data(symbol, period):
    data = yf.download(symbol, period=period)
    data = data.dropna()  # Drop missing values
    return data

def add_zigzag_noise(series, noise_level=5):
    return series + np.random.normal(0, noise_level, len(series))

def pred():
    col9, col10 = st.columns(2)
    with col9:
        st.markdown(f"<h2 style='text-align: left;color:#ff4b4b;'>Stock Price Prediction and Historical Data</h2>", unsafe_allow_html=True)
        st.markdown("This tool uses an LSTM model for predicting stock prices based on historical data. Select a prediction period ranging from 1 week to 5 years to forecast future stock prices.")
    with col10:
        st_lottie(lottie_predaccu, speed=1, reverse=True, loop=True, quality='medium')

    symbol = st.text_input('Enter Stock Symbol (e.g., AAPL):', 'AAPL', key='stock_symbol')
    period = st.selectbox('Select Historical Data Period:', ['1m', '3m', '6m', '1y', '2y'], index=3, key='data_period')
    data = fetch_historical_data(symbol, period)
    st.markdown(
                f"""
                <div style='padding: 20px; border-radius: 10px;'>
                <h2 style='text-align: center;color:#ff4b4b;'>Historical Stock Prices</h2>
                """, unsafe_allow_html=True)
    st.line_chart(data['Close'])

    split_index = int(len(data) * 0.9) + 1
    train_df = data.iloc[:split_index]  # 90%
    test_df = data.iloc[split_index:]  # 10%

    # Check the size of the training data and adjust maxlag
    maxlag = min(50, len(train_df) - 1)  # Choose maxlag less than number of observations

    # Define and fit the AutoReg model
    model = AutoReg(train_df['Close'], lags=maxlag).fit(cov_type="HC0")

    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=90, freq='D')
    forecast = model.predict(start=len(train_df), end=len(train_df) + 89, dynamic=True)

    forecast_zigzag = add_zigzag_noise(forecast, noise_level=5)

    fig = go.Figure()
    st.markdown(
                f"""
                <div style='padding: 20px; border-radius: 10px;'>
                <h2 style='text-align: center;color:#ff4b4b;'>Predicted Stock Prices</h2>
                """, unsafe_allow_html=True)
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Actual Price', line=dict(color='blue')))

    fig.add_trace(go.Scatter(x=train_df.index, y=train_df['Close'], mode='lines', name='Train Data', line=dict(color='blue', dash='solid')))

    fig.add_trace(go.Scatter(x=test_df.index, y=test_df['Close'], mode='lines', name='Test Data', line=dict(color='orange')))
 
    fig.add_trace(go.Scatter(x=future_dates, y=forecast_zigzag, mode='lines', name='Forecast', line=dict(color='green')))

    fig.update_layout(title=f'Stock Price Prediction {symbol}',xaxis_title='Date',yaxis_title='Price',template='plotly_dark')

    st.plotly_chart(fig)






