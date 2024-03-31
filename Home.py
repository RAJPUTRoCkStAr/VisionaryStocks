import streamlit as st
from streamlit_lottie import st_lottie
from lotti import lottie_company,lottie_hello
def home():
    st.title("Stock Price Prediction")
    hello = st_lottie(lottie_hello,speed=1,reverse=True,loop=True,quality='medium',height=180,width=180,key=None)
    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Purpose of making it")
        st.write("This abstract outlines the essence of stock price prediction, a vital aspect of financial markets. Leveraging historical data, mathematical models, and machine learning techniques, stock price prediction endeavors to forecast future movements in stock prices. By analyzing various factors such as market trends, company performance, economic indicators, and investor sentiment, predictive models aim to provide insights into potential price fluctuations. This abstract discusses the significance of accurate predictions for investors, traders, and financial institutions, highlighting the challenges and complexities inherent in forecasting stock prices. Through continuous refinement of algorithms and incorporation of new data sources, researchers and practitioners strive to enhance the accuracy and reliability of stock price prediction models, ultimately contributing to informed decision-making in the dynamic world of finance.")
    with col2:
        lottie_company
        comapny = st_lottie(lottie_company,speed=1,reverse=True,loop=True,quality='medium',height=None,width=None,key=None)