import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf
from streamlit_lottie import st_lottie
from lotti import lottie_exploredata
def explore():
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    col5,col6 = st.columns(2)
    with col5 :
        st.write("lets explore the data")
    with col6:
        lottie_exploredata
        exploredata = st_lottie(lottie_exploredata,speed=1,reverse=True,loop=True,quality='medium',height=None,width=None,key=None)

    companysymbol = st.text_input("Enter the symbol of company you want to explore")
    stock_symbol = companysymbol
    start_date = st.date_input("Start date from which date you want to explore")
    end_date = f"{current_year}-{current_month:02d}-01" 
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    explorebtn = st.button('Explore the data')
    if explorebtn:
        st.table(stock_data.head())
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Closing Price', line=dict(color='royalblue', width=2)))
        fig.update_layout(title=f'Stock Data for {stock_symbol}', xaxis_title='Date', yaxis_title='Price (USD)', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig)
    ticker = yf.Ticker(stock_symbol)
    company_info = {
        'Name': ticker.info.get('longName', 'N/A'),
        'Symbol': companysymbol,
        'Industry': ticker.info.get('industry', 'N/A'),
        'Sector': ticker.info.get('sector', 'N/A'),
        'Market Cap': ticker.info.get('marketCap', 'N/A'),
        'Previous Close': ticker.info.get('regularMarketPreviousClose', 'N/A'),
        'Open': ticker.info.get('regularMarketOpen', 'N/A'),
        'Dividend Yield': ticker.info.get('dividendYield', 'N/A'),
        'Currency': ticker.info.get('currency', 'N/A'),
        'P/E Ratio': ticker.info.get('trailingPE', 'N/A'),
        'Volume': ticker.info.get('volume', 'N/A'),
    }
    # for key, value in company_info.items():
    #     st.write(f'{key}: {value}')
    st.title(company_info['Name'])
    st.write(f"**Symbol:** {company_info['Symbol']}")
    st.write(f"**Industry:** {company_info['Industry']}")
    st.write(f"**Sector:** {company_info['Sector']}")
    st.write(f"**Market Cap:** {company_info['Market Cap']}")
    st.write(f"**Previous Close:** {company_info['Previous Close']}")
    st.write(f"**Open:** {company_info['Open']}")
    st.write(f"**Dividend Yield:** {company_info['Dividend Yield']}")
    st.write(f"**Currency:** {company_info['Currency']}")
    st.write(f"**P/E Ratio:** {company_info['P/E Ratio']}")
    st.write(f"**Volume:** {company_info['Volume']}")