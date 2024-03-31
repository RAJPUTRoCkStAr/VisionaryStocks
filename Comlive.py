import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime
import time
from streamlit_lottie import st_lottie
from lotti import lottie_report
def live():
    col11,col12 = st.columns(2)
    with col11:
        st.write("lets get the live data")
    with col12:
        lottie_report
        live = st_lottie(lottie_report,speed=1,reverse=True,loop=True,quality='medium',height=None,width=None,key=None)
    def get_stock_data(symbol):
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        return data
    fig = make_subplots(rows=1, cols=1)
    # Create Streamlit app
    st.title('Real-Time Stock Price')
    # Continuously update figure with new data
    while True:
        data = get_stock_data("AAPL")  # Example: Fetch data for Apple Inc. Replace "AAPL" with desired symbol
        trace = go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price')
        # Check if there are enough data points available
        if len(data) > 1:
            # Check if the latest price is higher or lower than the previous price
            if data['Close'].iloc[-1] > data['Close'].iloc[-2]:
                trace.line.color = 'green'  # Green line for increasing price
            else:
                trace.line.color = 'red'     # Red line for decreasing price
        fig.add_trace(trace)
        fig.update_layout(title='Real-Time Stock Price', xaxis_title='Time', yaxis_title='Price')
        # Display the Plotly figure in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        # Update every minute
        time.sleep(60)
