from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from streamlit_option_menu import option_menu
import streamlit as st
import random
import string
import smtplib
import sqlite3
import re
import base64
import os
import datetime as dt
import bcrypt  
from streamlit_lottie import st_lottie
from lotti import lottie_me
from dotenv import load_dotenv
load_dotenv()
import yfinance as yf
import sqlite3

#################################################################################
def title():
    st.set_page_config(page_title="VisionaryStocks ",layout="wide",page_icon='lotti/logo.png')
    title_webapp    = "VisionaryStocks"
    st.markdown(f"<h1 style='text-align: center;color:#ff4b4b;font-size:84px'>{title_webapp}</h1>", unsafe_allow_html=True)
    background_image = """
    <style>

    [data-testid="stAppViewContainer"] {
        # background-image: black !important;
        background-image: url("https://raw.githubusercontent.com/RAJPUTRoCkStAr/VisionaryStocks/main/data/bg.gif") !important;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed; /* Keep the background fixed during scrolling */
        height: 100vh; /* Full viewport height */
        width: 100vw; /* Full viewport width */
        overflow: hidden; /* Prevent scrolling for the container */
    }
    [data-testid="stSidebar"] {
        background-color: transparent;  /* Adds transparency to the sidebar */
        height: 100vh; /* Ensure sidebar height is the same as the viewport */
    }
    [data-testid="stHeader"] {
        background-color: transparent; /* Transparent header */
    }
    [data-testid="stToolbar"] {
        right: 2rem;
    }
    button[kind="sidebar"] {
        background-color:transparent;  /* Ensures sidebar button is transparent */
    }
    </style>
    """
    st.markdown(background_image, unsafe_allow_html=True)

#     st.markdown("""
#     <style>
#         .reportview-container {
#             margin-top: -2em;
#         }
#         #MainMenu {visibility: hidden;}
#         .stDeployButton {display:none;}
#         footer {visibility: hidden;}
#         #stDecoration {display:none;}
#         header {visibility: hidden;}
#     </style>
# """, unsafe_allow_html=True)

#######################################################################################
def generate_username(name):
    base_name = name.lower().replace(' ', '')
    random_suffix = ''.join(random.choices(string.digits, k=4))
    username = f"{base_name}{random_suffix}"
    return username

####################################################################
# Extract name from username
def extract_name(username):
    return ''.join(filter(str.isalpha, username))

#############################################################################
def adapt_date(date):
    return date.isoformat()

# Converter to convert from string to Python date
def convert_date(date_string):
    return dt.datetime.strptime(date_string, "%Y-%m-%d").date()
conn = sqlite3.connect('data/database.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    dob DATE,
    email TEXT, 
    username TEXT UNIQUE, 
    password TEXT)
''')
conn.commit()
sqlite3.register_adapter(dt.date, adapt_date)
sqlite3.register_converter("DATE", convert_date)
##############################################################################
def signup():
    conn = sqlite3.connect('data/database.db',detect_types=sqlite3.PARSE_DECLTYPES) 
    c = conn.cursor()
    today = dt.datetime.now()
    max_date = today - dt.timedelta(days=18*365)
    st.markdown(f"<h2 style='text-align: center;color:#ff4b4b'>Sign Up for VisionaryStocks</h2>", unsafe_allow_html=True)
    with st.form(key="signup_form", clear_on_submit=True):
        name = st.text_input("Enter your name")
        email = st.text_input("Enter your email address")
        dob = st.date_input("Enter your Date of Birth", max_value=max_date.date(), min_value=dt.datetime(1900, 1, 1).date())
        password = st.text_input("Enter your password", type="password")
        st.caption("Your password must be at least 7 characters in length and include a combination of uppercase and lowercase letters, numbers, and special characters.")
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if not name or not email or not password or not dob:
                st.error("Please fill in all required fields.")
            elif not re.match(r"^[A-Za-z\s]+$", name):
                st.error("Name should contain only alphabets and spaces.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address.")
            elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7,}$', password):
                st.error("Password must be at least 7 characters long and contain a mixture of symbols, capital letters, small letters, and numbers.")
            else:
                c.execute('''
                    SELECT * FROM users 
                    WHERE name = ? AND email = ?
                ''', (name, email))
                if c.fetchone():
                    st.error('A user with the same name and email already exists. Please try again.')
                else:
                    username = generate_username(name)
                    c.execute('SELECT * FROM users WHERE username = ?', (username,))
                    if c.fetchone() is None:
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Hash the password
                        c.execute('INSERT INTO users (name, dob, email, username, password) VALUES (?, ?, ?, ?, ?)', 
                                  (name, dob, email, username, hashed_password))
                        conn.commit()
                        send_thank_you_email(email, username, password, dob)
                    else:
                        st.error('Username already exists. Please try again.')

def send_thank_you_email(email, username, password, dob):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        if not smtp_username or not smtp_password:
            raise ValueError("SMTP credentials not set properly.")
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Welcome to Our Platform!'
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #1a73e8;">Welcome, {username}!</h1>
                <p>Thank you for registering with us. We're excited to have you on board!</p>
                <p>Your username: <strong>{username}</strong></p>
                <p>Your password: <strong>{password}</strong></p>
                <p>Your age :<strong>{dob}</strong></p>
                <p>To get started, you can now log in with your credentials and explore the platform.</p>
                <p>Best regards,<br>The Team</p>
                <hr style="border: 0; border-top: 1px solid #ddd;" />
                <footer>
                    <p style="font-size: 0.9em; color: #777;">
                        &copy; 2024 Our Company IAA. All rights reserved.<br>
                        <a href="http://example.com" style="color: #1a73e8; text-decoration: none;">Visit our website</a>
                    </p>
                </footer>
            </div>
        </body>
        </html>
        """
        message.attach(MIMEText(html, 'html'))
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        st.success(f"Congratulations, {username}! You have successfully registered for stocks with email {email}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")       

def login():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    st.markdown(f"<h2 style='text-align: center;color:#ff4b4b'>Log in Here 👇 for  VisionaryStocks</h2>", unsafe_allow_html=True)
    with st.form(key="login_form", clear_on_submit=True):
        username = st.text_input("Enter your username")
        password = st.text_input("Enter your password", type="password")
        login_button = st.form_submit_button("Login")
        forgot_password_button = st.form_submit_button("Forgot Password")
        
        if forgot_password_button:
            if username:
                c.execute('SELECT email FROM users WHERE username = ?', (username,))
                user_data = c.fetchone()
                if user_data:
                    email = user_data[0]
                    new_password = generate_custom_password()
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()) 
                    c.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, username))
                    conn.commit()
                    send_password_reset_email(email, new_password)
                else:
                    st.error("Username not found.")
            else:
                st.error("Please enter your username.")
        if login_button:
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                c.execute('SELECT password FROM users WHERE username = ?', (username,))
                user_data = c.fetchone()
                if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[0]):
                # if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[0]):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.password = password
                    st.session_state.page = "Dashboard"
                    st.success(f"Welcome back, {username}! You have successfully logged in. Enjoy managing your stocks.")
                    st.rerun()
                else:
                    st.error('Invalid username or password. Please try again.')

################################################################################

########################################################################################
def generate_custom_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choices(characters, k=length))
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7,}$', password):
            return password
#############################################################################
##############################################################################
def send_password_reset_email(email, new_password):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Password Reset Request'
        
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h1 style="color: #1a73e8; text-align: center;">Password Reset Successful</h1>
            <p>Dear User,</p>
            <p>We are pleased to inform you that your password has been successfully reset. Your new password is:</p>
            <h2 style="color: #333; text-align: center;"><strong>{new_password}</strong></h2>
            <p>Please use this new password to log in to your account. For security reasons, we recommend that you change your password immediately after logging in.</p>
            <p>If you did not request this password reset, please contact our support team immediately to secure your account.</p>
            <p>Best regards,<br>The Support Team</p>
            </div>
        </body>
        </html> 
        """
        message.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        
        st.success(f"A new password has been sent to {email}.")
    
    except Exception as e:
        st.error(f"Failed to send email: {e}")
#####################################################################################
def contactus():
        st.subheader("About Me: 👨‍💻")
        st.markdown("Hello, I'm Sumit Kumar Singh, a multifaceted developer with a keen interest in both data science and full-stack development. As the creator of the Stock price prediction App, I've leveraged my expertise in data science and machine learning to develop a robust solution for identifying and combating Stock price")
        st.markdown("Beyond data science, I'm deeply passionate about full-stack development, particularly with JavaScript and Python. With proficiency in both front-end and back-end technologies, I enjoy crafting seamless and intuitive user experiences while ensuring robust functionality and performance under the hood.")
        st.markdown("Whether I'm diving into the intricacies of machine learning algorithms or architecting scalable web applications, I approach each project with a combination of creativity, analytical rigor, and a relentless pursuit of excellence. My diverse skill set allows me to tackle complex challenges across the entire software development lifecycle, from ideation to deployment and beyond.")
        st.markdown("Driven by a thirst for knowledge and a commitment to continuous learning, I actively seek out opportunities to expand my expertise and stay at the forefront of technological advancements. Whether it's experimenting with new frameworks and libraries or contributing to open-source projects, I'm always eager to push the boundaries of what's possible in the world of software development.")
        st.markdown("Thank you for joining me on this exciting journey as I explore the intersection of data science, full-stack development, and beyond. Together, let's build innovative solutions that make a meaningful impact in the digital landscape.")
        st.markdown("Below are the links to connect with me")
        lottie_me
        Me = st_lottie(lottie_me, speed=1, reverse=True, loop=True, quality='medium', height=None, width=None, key=None)
        st.link_button("Linkedin", "https://www.linkedin.com/in/sumit-singh-773921262/", use_container_width=True,type="primary")
        st.link_button("Kaggle", "https://www.kaggle.com/sumitkumarsingh22002", use_container_width=True,type="primary")
        st.link_button("Github", "https://github.com/RAJPUTRoCkStAr", use_container_width=True,type="primary")
################################################################################
#changer username
def change_username():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    try:
        current_username = st.session_state.username
        showing_username = st.text_input("showing current username",value=current_username,disabled=True)
        new_username = st.text_input("Enter your new username")
        change_username_btn = st.button("Change Username",type="primary")
        
        if change_username_btn:
            if new_username:
                c.execute('SELECT email, FROM users WHERE username = ?', (current_username,))
                user_data = c.fetchone()
                
                if user_data:
                    email= user_data
                    workplace = st.session_state.item
                    c.execute('SELECT username FROM users WHERE username = ?', (new_username, workplace))
                    if c.fetchone():
                        st.error("The new username is already taken within your workplace. Please choose another one.")
                    else:
                        c.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, current_username))
                        conn.commit()
                        st.session_state.username = new_username
  
                        st.success("Username changed successfully!")
                        send_username_change_email(email, new_username)
            else:
   
                st.error("New username cannot be empty.")
    
    except Exception as e:

        st.error(f"An error occurred: {e}")
    
    finally:
        conn.close()

def send_username_change_email(email, new_username):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Username Change Notification'
        
        html = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #1a73e8;">Username Changed Successfully</h1>
                <p>Hello,</p>
                <p>Your username has been successfully changed to <strong>{new_username}</strong>.</p>
                <p>If you did not request this change, please contact our support team immediately.</p>
                <p>Best regards,<br>The Team</p>
            </div>
        </body>
        </html>
        """
        message.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        

        st.success(f"A notification email has been dispatched to {email} concerning your username change request.")
    
    except Exception as e:
        
        st.error(f"Failed to send email: {e}")
################################################################
#################################################################################
#Change Password
def changepass():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    
    # Fetch the username from session
    username = st.session_state.username
    c.execute('SELECT email, password FROM users WHERE username = ?', (username,))
    user_data = c.fetchone()
    
    if user_data:
        email, hashed_current_password = user_data
        
        # Ensure that hashed_current_password is bytes
        if isinstance(hashed_current_password, str):
            hashed_current_password = hashed_current_password.encode('utf-8')
        
        # Create the form for changing the password
        with st.form(key="change_password_form", clear_on_submit=True):
            old_password = st.text_input("Enter your current password", type="password")
            new_password = st.text_input("Enter your new password", type="password")
            confirm_new_password = st.text_input("Confirm your new password", type="password")
            st.caption("New password must be at least 7 characters long and include a combination of uppercase and lowercase letters, numbers, and special characters.")
            change_password = st.form_submit_button("Change Password", type="primary")
            
            if change_password:
                # Convert old_password (user input) to bytes
                old_password_bytes = old_password.encode('utf-8')
                
                # Check if the old password matches the hashed password in the database
                if not bcrypt.checkpw(old_password_bytes, hashed_current_password):
                    st.error("Your current password is incorrect. Please try again.")
                
                # Check if the new password matches the required format
                elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7,}$', new_password):
                    st.error("New password must be at least 7 characters long and contain a mixture of symbols, capital letters, small letters, and numbers.")
                
                # Check if the new password matches the confirmation password
                elif new_password != confirm_new_password:
                    st.error("New password and confirmation do not match. Please try again.")
                
                else:
                    # Hash the new password before saving it
                    hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    # Update the password in the database
                    c.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_new_password, username))
                    conn.commit()
                    
                    st.success("Password changed successfully!")
                    send_password_change_email(email)
                    
                    # Update the password in the session state
                    st.session_state.password = new_password
    else:
        st.error("User data not found.")
    
    conn.close()
def send_password_change_email(email):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = 'Password Change Notification'
        
        html = """
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #1a73e8;">Password Changed Successfully</h1>
                <p>Hello,</p>
                <p>Your password has been successfully changed. If you did not request this change, please contact our support team immediately.</p>
                <p>Best regards,<br>The Team</p>
            </div>
        </body>
        </html>
        """
        message.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        st.success(f"A notification email has been dispatched to {email} concerning your password change request.")
    
    except Exception as e:
        st.error(f"Failed to send email: {e}")
##########################################################################
##################################################################################
def profilesetting():
    st.markdown(f"<h2 style='text-align: center;color:#ff4b4b'>Profile Setting</h2>", unsafe_allow_html=True)
    selected2 = option_menu(None, ["Change Username", "Change Password"], 
    icons=['fill-person-fill', "passport"], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    if selected2 == "Change Username":
        change_username()
    if selected2 == "Change Password":
        changepass()



