import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim
import yfinance as yf   
from streamlit_folium import folium_static
from streamlit_lottie import st_lottie
from lotti import lottie_map
def map():
    col7,col8 = st.columns(2)
    with col7:
        st.header("Explore Company Headquarters Location",divider='rainbow')
        st.write(" Welcome to the Company Headquarters Location Explorer! This tool allows you to discover the geographical location of a company's headquarters. Simply enter the company's ticker symbol and explore its headquarters on the map. Gain valuable insights into the company's presence and explore its location in the context of its operations. Whether you're a researcher, investor, or curious individual, this tool offers a user-friendly platform for exploring the geographical footprint of companies. Start exploring now and gain valuable insights into the locations where companies operate."
        )
    with col8:
        lottie_map
        map = st_lottie(lottie_map,speed=1,reverse=True,loop=True,quality='medium',height=None,width=None,key=None)
    
    ticker_symbol = st.text_input("Enter the symbol of the company you want to see on map")
    if ticker_symbol:
        company = yf.Ticker(ticker_symbol)
        company_info = {
            'city': company.info.get('city', 'N/A'),
            'state': company.info.get('state', 'N/A'),
            'country': company.info.get('country', 'N/A'),
            'zip': company.info.get('zip', 'N/A'),
        }
        geolocator = Nominatim(user_agent="Stock-Prediction")
        address = f"{company_info['city']}, {company_info['state']}, {company_info['country']}"
        location = geolocator.geocode(address)
        if location:
            latitude, longitude = location.latitude, location.longitude
            st.subheader(f"Your Company Symbol is {ticker_symbol} and country is {company_info['country']} and city is {company_info['city']}")
            folium_map = folium.Map(location=[latitude, longitude], zoom_start=10, tiles='OpenStreetMap')
            folium.Marker(
                [latitude, longitude],
                popup=f'{ticker_symbol} Headquarters',
                tooltip='Click for more info'
                ).add_to(folium_map)
            folium_static(folium_map)   
        else:
            st.write("Coordinates not found for the company's location.") 
