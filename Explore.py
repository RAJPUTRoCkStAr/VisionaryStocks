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

    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("Discover Company Stock Data Exploration",divider='rainbow')
        st.write(
            "Welcome to the Stock Data Exploration Tool! This interactive application empowers users to delve into historical stock data effortlessly. By inputting the stock symbol and selecting a start date, users can unlock a wealth of insights into stock price movements and company performance. With a simple click, users can explore visual representations of stock prices plotted over their selected time frame, enabling them to identify trends and patterns with ease. Beyond visualizations, users can access crucial company information, including industry, sector, market capitalization, dividend yield, currency, P/E ratio, and trading volume, providing valuable context for informed decision-making. Whether you're a seasoned investor seeking to analyze market trends or a curious individual interested in exploring stock data, this tool offers a user-friendly platform for insightful exploration of the dynamic world of finance. Start exploring now and gain valuable insights into the complexities of the stock market!"
        )

    with col2:
        lottie_exploredata
        exploredata = st_lottie(
            lottie_exploredata,
            speed=1,
            reverse=True,
            loop=True,
            quality="medium",
            height=None,
            width=None,
            key=None,
        )
    global stock_symbol
    stock_symbol = st.text_input("Enter the symbol of the company you want to explore")
    st.info("You need to choose starting date ")
    start_date = st.date_input("Start date from which date you want to explore")

    explorebtn = st.button("Explore the data",use_container_width=True,type="primary")
    if explorebtn:
        end_date = f"{current_year}-{current_month:02d}-01"
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        if not stock_data.empty:
            st.table(stock_data.head())
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=stock_data.index,
                    y=stock_data["Close"],
                    mode="lines",
                    name="Closing Price",
                    line=dict(color="red", width=2),
                )
            )
            fig.update_layout(
                title=f"Stock Data for {stock_symbol}",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig)

        ticker = yf.Ticker(stock_symbol)
        company_info = {
            "Name": ticker.info.get("longName", "N/A"),
            "Symbol": stock_symbol,
            "Industry": ticker.info.get("industry", "N/A"),
            "Sector": ticker.info.get("sector", "N/A"),
            "Market Cap": ticker.info.get("marketCap", "N/A"),
            "Previous Close": ticker.info.get("regularMarketPreviousClose", "N/A"),
            "Open": ticker.info.get("regularMarketOpen", "N/A"),
            "Dividend Yield": ticker.info.get("dividendYield", "N/A"),
            "Currency": ticker.info.get("currency", "N/A"),
            "P/E Ratio": ticker.info.get("trailingPE", "N/A"),
            "Volume": ticker.info.get("volume", "N/A"),
            "Country": ticker.info.get("country", "N/A"),
            "Website": ticker.info.get("website", "N/A")
        }
        st.title("Company Information")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("**Name:**")
            st.write(company_info["Name"])
        with col2:
            st.markdown("**Symbol:**")
            st.write(company_info["Symbol"])
        with col3:
            st.markdown("**Industry:**")
            st.write(company_info["Industry"])
        with col4:
            st.markdown("**Sector:**")
            st.write(company_info["Sector"])
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.markdown("**Market Cap:**")
            st.write(f"${company_info['Market Cap']:,}")
        with col6:
            st.markdown("**Previous Close:**")
            st.write(f"${company_info['Previous Close']}")
        with col7:
            st.markdown("**Open:**")
            st.write(f"${company_info['Open']}")
        with col8:
            st.markdown("**Dividend Yield:**")
            st.write(f"{company_info['Dividend Yield']}")
        col9, col10, col11, col12 = st.columns(4)
        with col9:
            st.markdown("**Currency:**")
            st.write(company_info["Currency"])
        with col10:
            st.markdown("**P/E Ratio:**")
            st.write(company_info["P/E Ratio"])
        with col11:
            st.markdown("**Volume:**")
            st.write(f"{company_info['Volume']}")
        with col12:
            st.markdown("**Country:**")
            st.write(f"{company_info['Country']}")
        st.title("Additional Information")
        col13, col14 = st.columns(2)
        with col13:
            st.markdown("**Website:**")
            website = company_info['Website']
            link = st.link_button("Website",website,type="primary")
        with col14:
            st.markdown("**Last Updated:**")
            st.write(current_date.strftime("%Y-%m-%d %H:%M:%S"))
