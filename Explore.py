import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import yfinance as yf
from streamlit_lottie import st_lottie
from lotti import lottie_exploredata
import plotly.express as px
from datetime import datetime
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium
import numpy as np
def explore():
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("Discover Company Stock Data Exploration", divider='rainbow')
        st.write(
            "Welcome to the Stock Data Exploration Tool! This interactive application empowers users to delve into historical stock data effortlessly..."
        )
    with col2:
        st_lottie(lottie_exploredata, speed=1, reverse=True, loop=True, quality="medium")

    time_range_map = {
        "1d": ("1d", "1m"),
        "5d": ("5d", "5m"),
        "1mo": ("1mo", "1d"),
        "6mo": ("6mo", "1wk"),
        "1y": ("1y", "1d"),
        "5y": ("5y", "1mo"),
        "all": ("max", "3mo")
    }
    
    time_range_options = ["1 Day", "5 Days", "1 Month", "6 Months", "1 Year", "5 Years", "Max"]
    time_range_keys = ["1d", "5d", "1mo", "6mo", "1y", "5y", "all"]
    selected_time_range = st.selectbox("Select Time Range", time_range_options)
    period, interval = time_range_map[time_range_keys[time_range_options.index(selected_time_range)]]
    
    ticker = st.text_input('Enter Stock Ticker').upper().strip()
    ticker_button = st.button('Explore')
    if ticker_button:
        stock_data = yf.download(ticker, period=period, interval=interval)
        
        if not stock_data.empty:
            with st.container():
                st.markdown(
                    f"""
                    <div style='padding: 20px; border-radius: 10px;'>
                        <h2 style='text-align: center;'>Stock Price Summary - {ticker.upper()}</h2>
                    """, unsafe_allow_html=True)
                st.header(f"{stock_data.Close.iloc[-1]:.2f}")
                p_d = stock_data.Close.iloc[-1] - stock_data.Open.iloc[0]
                pd_p = (p_d / stock_data.Open.iloc[0]) * 100
                color = "green" if p_d >= 0 else "red"
                st.markdown(f"<h1 style='color:{color};font-size: 15px;padding:0px'>{p_d:.2f} ({pd_p:.2f}%)</h1>", unsafe_allow_html=True)
                st.write("</div>", unsafe_allow_html=True)
            
            st.write('Stock Data Viewer with Various Charts')
            fig = px.line(stock_data, x=stock_data.index, y='Close', title=f'{ticker} Price Over Time')
            st.plotly_chart(fig)
            
            app = option_menu(None, ["Performance Metrics", "Fundamental Data"], orientation='horizontal')        

            if app == 'Performance Metrics':
                with st.container():
                    st.markdown(
                        """
                        <div style='padding: 20px; border-radius: 10px;'>
                            <h3 style='text-align: center;'>Performance Metrics</h3>
                            <hr style='border: 1px solid #ccc;'>
                        """, unsafe_allow_html=True)
                    
                    data2 = stock_data.copy()
                    data2['% Change'] = stock_data['Adj Close'] / stock_data['Adj Close'].shift(1) - 1
                    data2.dropna(inplace=True)
                    st.dataframe(data2,use_container_width=True,height=640)        
                    annual_return = data2['% Change'].mean() * 252 * 100
                    stdev = np.std(data2['% Change']) * np.sqrt(252)
                    risk_adj_return = annual_return / stdev if stdev != 0 else 0
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        growth_symbol = lambda x: "📈" if x > 0 else "📉" if x < 0 else ""
                        st.header(f"{annual_return:.2f}% {growth_symbol(annual_return)}")
                        st.write("Annual Return (%)")
                    with col2:
                        st.header(f"{stdev * 100:.2f}% {growth_symbol(stdev)}")
                        st.write('Standard Deviation (%)')
                    with col3:
                        st.header(f"{risk_adj_return:.2f} {growth_symbol(risk_adj_return)}")
                        st.write('Risk Adj. Return')
                        
                    st.write("</div>", unsafe_allow_html=True)    
            elif app == 'Fundamental Data':
                st.info("You need to choose a starting date ")
                start_date = st.date_input("Start date from which date you want to explore", value=datetime(current_year, current_month, 1))
                explorebtn = st.button("Explore the data", use_container_width=True, type="primary")
                if explorebtn:
                    end_date = f"{current_year}-{current_month:02d}-01"
                    stock_data = yf.download(ticker, start=start_date, end=end_date)
                    
                    company_info = yf.Ticker(ticker).info
                    company_info_display = {
                        "Name": company_info.get("longName", "N/A"),
                        "Symbol": ticker,
                        "Industry": company_info.get("industry", "N/A"),
                        "Sector": company_info.get("sector", "N/A"),
                        "Market Cap": company_info.get("marketCap", "N/A"),
                        "Previous Close": company_info.get("regularMarketPreviousClose", "N/A"),
                        "Open": company_info.get("regularMarketOpen", "N/A"),
                        "Dividend Yield": company_info.get("dividendYield", "N/A"),
                        "Currency": company_info.get("currency", "N/A"),
                        "P/E Ratio": company_info.get("trailingPE", "N/A"),
                        "Volume": company_info.get("volume", "N/A"),
                        "Country": company_info.get("country", "N/A"),
                        "Website": company_info.get("website", "N/A")
                    }            
                    st.title("Company Information")
                    num_columns = 3
                    num_rows = (len(company_info_display) + num_columns - 1) // num_columns 
                    for i in range(num_rows):
                        columns = st.columns(num_columns)
                        for j in range(num_columns):
                            index = i * num_columns + j
                            if index < len(company_info_display):
                                key, value = list(company_info_display.items())[index]
                                if key == "Website" and value != "N/A":
                                    value = f"<a href='{value}' target='_blank' class='link-button'>{value}</a>"
                                with columns[j]:
                                    st.markdown(f"""
                                    <div class="card">
                                        <div class="card-title">{key}:</div>
                                        <div class="card-content">{value}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                    st.markdown(
                        """
                        <style>
                        .card-container {
                            display: flex;
                            flex-wrap: wrap;
                            gap: 20px;
                            justify-content: space-between;
                        }
                        .card {
                            background: linear-gradient(135deg, #f0f4f8, #ffffff);
                            border-radius: 15px;
                            padding: 20px;
                            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
                            flex: 1 1 30%;
                            min-width: 250px;
                            transition: all 0.3s ease;
                        }
                        .card:hover {
                            transform: scale(1.05);
                            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                        }
                        .card-title {
                            font-size: 18px;
                            font-weight: bold;
                            color: #333;
                            margin-bottom: 10px;
                        }
                        .card-content {
                            font-size: 16px;
                            color: #555;
                            margin-bottom: 10px;
                        }
                        .link-button {
                            color: #1a0dab;
                            text-decoration: none;
                            font-weight: bold;
                        }
                        .link-button:hover {
                            text-decoration: underline;
                        }
                        </style>
                        """, unsafe_allow_html=True)

                    if company_info.get("city") and company_info.get("country"):
                        geolocator = Nominatim(user_agent="stock-explorer")
                        location = geolocator.geocode(f"{company_info['city']}, {company_info['country']}")
                        if location:
                            folium_map = folium.Map(location=[location.latitude, location.longitude], zoom_start=10)
                            folium.Marker([location.latitude, location.longitude], popup=f'{ticker} Headquarters').add_to(folium_map)
                            folium_static(folium_map)
                        else:
                            st.warning("Coordinates not found for the company's location.")
