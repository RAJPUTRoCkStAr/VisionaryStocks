import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime
import time
from streamlit_lottie import st_lottie
from lotti import lottie_report

def live():
    col11, col12 = st.columns(2)
    with col11:
        st.write("In the digital realm of financial markets, real-time data streams provide a window into the ever-changing landscape of stock prices. Amidst the flow of information, an individual embarks on a journey to navigate the complexities of market dynamics. Fueled by a desire for insight, they harness the power of technology to visualize trends and patterns. Through the interplay of candlestick charts and moving averages, they seek to uncover the underlying rhythms of market behavior. As the data unfolds, each fluctuation becomes a thread in the tapestry of market sentiment. In this quest for understanding, they embrace the challenge of deciphering signals amidst the noise. And in the dance between data and interpretation, they find both the exhilaration of discovery and the humbling reminder of the unpredictable nature of markets.")
    with col12:
        lottie_report
        live = st_lottie(lottie_report, speed=1, reverse=True, loop=True, quality='medium', height=None, width=None, key=None)
    st.title('Real-Time Stock Price Visualization')
    
    ticker = st.text_input("Enter stock symbol for marking")
    if ticker:
            data = yf.download(ticker, period='1d', interval='1m')
            fig = make_subplots(rows=1, cols=1)
        
            fig = go.Figure(data=go.Candlestick(x=data.index,
                                                 open=data['Open'],
                                                 high=data['High'],
                                                 low=data['Low'],
                                                 close=data['Close']))
        
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(20).mean(), name='20-day MA', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(50).mean(), name='50-day MA', line=dict(color='orange')))
        
            fig.update_layout(title='Real-Time Stock Price for {}'.format(ticker),
                              xaxis_title='Date',
                              yaxis_title='Price',
                              template='plotly_dark',
                              margin=dict(l=50, r=50, t=50, b=50),
                              paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='white'))
        
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
        
            st.plotly_chart(fig)
