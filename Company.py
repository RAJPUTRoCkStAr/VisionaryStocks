import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
from lotti import lottie_company
def company():
    st.header("list of company and explore company")
    col3,col4 = st.columns(2)
    with col3 :
        st.write("Explore Companies:\n Welcome to the Company Exploration App! Select the column from your existing dataset that contains company names or related information. From there, choose an industry from the dropdown menu to view companies associated with that industry. You'll be able to explore additional details such as symbols or other relevant information for each company. Whether you're conducting market research, analyzing industry trends, or seeking investment opportunities, this app provides a convenient way to delve into the world of companies within your dataset. Start exploring now and uncover valuable insights!")
    with col4:
        lottie_company
        comapny = st_lottie(lottie_company,speed=1,reverse=True,loop=True,quality='medium',height=None,width=None,key=None)
    st.subheader("explore company name and symbol with industrial name")
    df = pd.read_csv("fdata.csv", encoding='latin-1') 
    st.subheader("Industry we have to select form is :")
    selected_industry = st.selectbox("Select an industry", df['Industry'].unique())
    st.subheader(f"The industry you selected is {selected_industry} and the company and symbol are listed below")
    if selected_industry:
        selected_data = df[df['Industry'] == selected_industry][['Company Name', 'Symbol']]
        selected_data.reset_index(drop=True, inplace=True)
        selected_data.index += 1  # Start index from 1
        st.write("Companies in selected industry:")
        st.table(selected_data)