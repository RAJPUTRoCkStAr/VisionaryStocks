import streamlit as st
from streamlit_option_menu import option_menu
from Home import home
from Company import company
from Explore import explore
from utils import signup, login,title
from Dash import dashboard
from News import news
from Stocktrends import Stocktre
title()
# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Home"

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        if st.session_state.logged_in:
            dashboard()  # Show dashboard if logged in
        else:
            with st.sidebar:
                app = option_menu(
                    menu_title="Main Menu",
                    options=[
                        'Home',
                        'Company',
                        'Stock News',
                        'Stock Market Trends',
                        'Login',
                        'Sign Up'
                    ],
                    icons=['house', 'building', 'newspaper','lock', 'person'],
                    menu_icon="cast"
                )

            # Redirect to corresponding page based on menu selection
            if app == "Home":
                home()
            elif app == "Company":
                company()
            elif app == "Explore":
                explore()
            elif app == 'Stock News':
                news()
            elif app == 'Stock Market Trends':
                Stocktre()
            elif app == 'Login':
                login()
            elif app == 'Sign Up':
                signup()

app = MultiApp()
app.run()
