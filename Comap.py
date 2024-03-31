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
        st.write("map")
    with col8:
        lottie_map
        map = st_lottie(lottie_map,speed=1,reverse=True,loop=True,quality='medium',height=None,width=None,key=None)
    st.title('Company Headquarters Location')
    ticker_symbol = "ATS"  
    company = yf.Ticker(ticker_symbol)
    company_info = {
        'city': company.info.get('city', 'N/A'),
        'state': company.info.get('state', 'N/A'),
        'country': company.info.get('country', 'N/A'),
        'zip': company.info.get('zip', 'N/A'),
    }
    geolocator = Nominatim(user_agent="my_geocoder")
    address = f"{company_info['city']}, {company_info['state']}, {company_info['country']}"
    location = geolocator.geocode(address)
    
    if location:
        latitude, longitude = location.latitude, location.longitude
        folium_map = folium.Map(location=[latitude, longitude], zoom_start=10, tiles='OpenStreetMap')
        folium.Marker(
            [latitude, longitude],
            popup=f'{ticker_symbol} Headquarters',
            tooltip='Click for more info'
        ).add_to(folium_map)
        folium_static(folium_map)
        
        st.markdown(f"**Company Headquarters Location:** {latitude}, {longitude}")   
    else:
        st.write("Coordinates not found for the company's location.") 