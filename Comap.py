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
     
