import streamlit as st
from streamlit_option_menu import option_menu
from Home import home
from Company import company
from Explore import explore
from utils import signup, login,title
from Dash import dashboard
from News import news
from Stocktrends import Stocktre
import bcrypt
from utils import admin_login
from Admin import view_database
title()

# query_params = st.experimental_get_query_params()
query_params = st.query_params
page = query_params.get("page", ["home"])[0]
admin_code = query_params.get("admin_code", [None])[0]

if admin_code == "22":
    st.session_state.admin_mode = True
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False
if 'log_in' not in st.session_state:
    st.session_state.log_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Home"


if st.session_state.admin_mode:
    if not st.session_state.log_in:
        admin_login()  
        if st.session_state.log_in:
            st.experimental_set_query_params(admin_code="456", page="view_database")
            st.experimental_rerun()  
    else:
        view_database()  
        st.stop()  
if st.session_state.logged_in:
    dashboard()  
    st.stop()  

if not st.session_state.logged_in and not st.session_state.admin_mode:
            with st.sidebar:
                app = option_menu(
                    None,
                    options=[
                    'Home',
                    'Company',
                    'Stock News',
                    'Stock Market Trends',
                    'Login',
                    'Sign Up'
                    ],
                    icons=[
                        'house-fill',             # Home icon
                        'building-fill',          # Company icon
                        'newspaper',         # Stock News icon
                        'graph-up-arrow',          # Stock Market Trends icon
                        'box-arrow-in-right',# Login icon
                        'person-plus-fill'        # Sign Up icon
                    ],
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


