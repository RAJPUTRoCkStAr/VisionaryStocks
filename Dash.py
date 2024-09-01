import streamlit as st
import sqlite3
import Home,Company,Explore,Comap,Compre,Comlive
from streamlit_option_menu import option_menu
from utils import extract_name, adapt_date,profilesetting
import datetime as dt
def convert_date(date_bytes):
    if isinstance(date_bytes, bytes):
        date_bytes = date_bytes.decode('utf-8')  # Convert bytes to string
    return dt.datetime.strptime(date_bytes, "%Y-%m-%d").date()

sqlite3.register_adapter(dt.date, adapt_date)
sqlite3.register_converter("DATE", convert_date)
def dashboard():
    st.write("Under process")
    with st.sidebar:      
            app = option_menu(
                        menu_title="Main Menu",
                        options=[
                                'main',
                                'Explore',
                                'Map',
                                'Prediction',
                                'Stocks',
                                'Profile Setting',
                                'Log Out'
                                ],
                                icons=['house', 'binoculars', 'map', 'graph-up', 'bar-chart', 'tools','box-arrow-right'],
                                menu_icon="cast"
                        ) 
    if app == "main":
        conn = sqlite3.connect('data/database.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
    
        username = st.session_state.get('username')
        if username:
            name = extract_name(username)
            c.execute('SELECT email, dob, password FROM users WHERE username = ?', (username,))
            user_data = c.fetchone()

            if user_data:
                email, dob, current_password = user_data
                if dob:
                    today = dt.date.today()
                    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                else:
                    age = "N/A"

                st.markdown(f"<h2 style='text-align: center;'>Personal Information</h2>", unsafe_allow_html=True)
                st.markdown("<hr style='border-top: 2px solid #bbb;'>", unsafe_allow_html=True)
                st.markdown(f"**👤 Username:** `{username}`")
                st.markdown(f"**📧 Email:** `{email}`")
                st.markdown(f"**🎂 Date of Birth:** `{dob}`")
                st.markdown(f"**🗓️ Age:** `{age}`")
                st.markdown("<hr style='border-top: 2px solid #bbb;'>", unsafe_allow_html=True)
            else:
                st.error("User data not found.")

        else:
            st.error("No user is logged in.")

    if app == "Explore":
            Explore.explore()
    if app == "Map":
            Comap.map()
    if app == "Prediction":
            Compre.pred()
    if app == "Stocks":
            Comlive.live()
    elif app == "Profile Setting":
        profilesetting()
    
    if app == "Log Out":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.page = "Home"
        st.rerun()
