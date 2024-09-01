# import streamlit as st
# import pandas as pd
# import numpy as np
# import yfinance as yf
# import plotly.graph_objs as go
# from statsmodels.tsa.ar_model import AutoReg
# import datetime as dt

# def fetch_historical_data(symbol, period):
#     data = yf.download(symbol, period=period)
#     data = data.dropna()  # Drop missing values
#     return data

# def add_zigzag_noise(series, noise_level=5):
#     return series + np.random.normal(0, noise_level, len(series))

# def pred():
#     col9, col10 = st.columns(2)
#     with col9:
#         st.header("Stock Price Prediction and Historical Data", divider='rainbow')
#         st.markdown("This tool uses an LSTM model for predicting stock prices based on historical data. Select a prediction period ranging from 1 week to 5 years to forecast future stock prices.")
#     with col10:
#         pass
#         # st_lottie(lottie_predaccu, speed=1, reverse=True, loop=True, quality='medium')

#     def fetch_historical_data(symbol, period):
#         data = yf.download(symbol, period=period)
#         data = data.dropna()  # Drop missing values
#         return data

#     st.header('Stock Price Prediction', divider='rainbow')
#     symbol = st.text_input('Enter Stock Symbol (e.g., AAPL):', 'AAPL')
#     period = st.selectbox('Select Historical Data Period:', ['1m', '3m', '6m', '1y', '2y'], index=3)
#     data = fetch_historical_data(symbol, period)
#     st.subheader('Historical Stock Prices')
#     st.line_chart(data['Close'])

#     # Load historical stock data
#     symbol = st.text_input('Enter Stock Symbol (e.g., AAPL):', 'AAPL')
#     period = st.selectbox('Select Period:', ['1m', '3m', '6m', '1y', '2y'], index=3)
#     stock_data_hist = fetch_historical_data(symbol, period)

#     # Define training and testing areas
#     split_index = int(len(stock_data_hist) * 0.9) + 1
#     train_df = stock_data_hist.iloc[:split_index]  # 90%
#     test_df = stock_data_hist.iloc[split_index:]  # 10%

#     # Check the size of the training data and adjust maxlag
#     maxlag = min(50, len(train_df) - 1)  # Choose maxlag less than number of observations

#     # Define and fit the AutoReg model
#     model = AutoReg(train_df['Close'], lags=maxlag).fit(cov_type="HC0")

#     future_dates = pd.date_range(start=stock_data_hist.index[-1] + pd.Timedelta(days=1), periods=90, freq='D')
#     forecast = model.predict(start=len(train_df), end=len(train_df) + 89, dynamic=True)

#     forecast_zigzag = add_zigzag_noise(forecast, noise_level=5)

#     fig = go.Figure()

#     fig.add_trace(go.Scatter(x=stock_data_hist.index, y=stock_data_hist['Close'], mode='lines', name='Actual Price', line=dict(color='blue')))

#     fig.add_trace(go.Scatter(x=train_df.index, y=train_df['Close'], mode='lines', name='Train Data', line=dict(color='blue', dash='solid')))

#     fig.add_trace(go.Scatter(x=test_df.index, y=test_df['Close'], mode='lines', name='Test Data', line=dict(color='orange')))
 
#     fig.add_trace(go.Scatter(x=future_dates, y=forecast_zigzag, mode='lines', name='Forecast', line=dict(color='green')))

#     fig.update_layout(title=f'Stock Price Prediction with Zigzag Pattern for {symbol}',xaxis_title='Date',yaxis_title='Price',template='plotly_dark')

#     st.plotly_chart(fig)


import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
from statsmodels.tsa.ar_model import AutoReg
import datetime as dt

def fetch_historical_data(symbol, period):
    data = yf.download(symbol, period=period)
    data = data.dropna()  # Drop missing values
    return data

def add_zigzag_noise(series, noise_level=5):
    return series + np.random.normal(0, noise_level, len(series))

def pred():
    col9, col10 = st.columns(2)
    with col9:
        st.header("Stock Price Prediction and Historical Data", divider='rainbow')
        st.markdown("This tool uses an LSTM model for predicting stock prices based on historical data. Select a prediction period ranging from 1 week to 5 years to forecast future stock prices.")
    with col10:
        pass
        # st_lottie(lottie_predaccu, speed=1, reverse=True, loop=True, quality='medium')

    st.header('Stock Price Prediction', divider='rainbow')
    
    # Unique keys added to widgets
    symbol = st.text_input('Enter Stock Symbol (e.g., AAPL):', 'AAPL', key='stock_symbol')
    period = st.selectbox('Select Historical Data Period:', ['1m', '3m', '6m', '1y', '2y'], index=3, key='data_period')
    data = fetch_historical_data(symbol, period)
    st.subheader('Historical Stock Prices')
    st.line_chart(data['Close'])

    # Define training and testing areas
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

    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Actual Price', line=dict(color='blue')))

    fig.add_trace(go.Scatter(x=train_df.index, y=train_df['Close'], mode='lines', name='Train Data', line=dict(color='blue', dash='solid')))

    fig.add_trace(go.Scatter(x=test_df.index, y=test_df['Close'], mode='lines', name='Test Data', line=dict(color='orange')))
 
    fig.add_trace(go.Scatter(x=future_dates, y=forecast_zigzag, mode='lines', name='Forecast', line=dict(color='green')))

    fig.update_layout(title=f'Stock Price Prediction with Zigzag Pattern for {symbol}',xaxis_title='Date',yaxis_title='Price',template='plotly_dark')

    st.plotly_chart(fig)






