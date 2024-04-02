import streamlit as st
from streamlit_option_menu import option_menu
import Home,Company,Explore,Comap,Compre,Comlive

st.set_page_config(
                page_title="Stock Prediction App",
                page_icon=":chart_with_upwards_trend:",
                layout="wide")
class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })
    def run():
        with st.sidebar:      
                app = option_menu(
                        menu_title="Main Menu",
                        options=[
                                'Home',
                                'Company',
                                'Explore',
                                'Map',
                                'Prediction',
                                'Stocks'
                                ],
                                icons=['house-fill', 'journal','file-bar-graph-fill','geo-alt','graph-up-arrow','diamond-fill'],
                                menu_icon="cast"
                        ) 
        if app == "Home":
            Home.home()
        if app == "Company":
            Company.company()
        if app == "Explore":
            Explore.explore()
        if app == "Map":
            Comap.map()
        if app == "Prediction":
            Compre.pred()
        if app == "Stocks":
            Comlive.live()
    run()   