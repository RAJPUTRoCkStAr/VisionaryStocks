import streamlit as st
from bs4 import BeautifulSoup as BS
import requests as req

def news():
    urls = {
        "Union Budget": "https://www.businesstoday.in/union-budget",
        "Drive Today (BT TV)": "https://www.businesstoday.in/bt-tv/drive-today",
        "Market Today (BT TV)": "https://www.businesstoday.in/bt-tv/market-today",
        "Insurance": "https://www.businesstoday.in/personal-finance/insurance",
        "Investment": "https://www.businesstoday.in/personal-finance/investment",
        "Enterprise Tech": "https://www.businesstoday.in/tech-today/enterprise-tech",
        "Tech Explainers": "https://www.businesstoday.in/tech-today/explainers",
        "Tax": "https://www.businesstoday.in/personal-finance/tax",
        "IPO Corner": "https://www.businesstoday.in/markets/ipo-corner",
        "Stocks": "https://www.businesstoday.in/markets/stocks",
        "Company Stock": "https://www.businesstoday.in/markets/company-stock",
        "Economy": "https://www.businesstoday.in/latest/economy",
        "Trending Stocks": "https://www.businesstoday.in/markets/trending-stocks"
    }
    
    selected = st.selectbox("Select a Category", list(urls.keys()))
    
    st.markdown(f"<h1 style='text-align: center; color: #2c3e50;'>{selected} Headlines</h1>", unsafe_allow_html=True)
    st.write("---")

    url = urls[selected]
    webpage = req.get(url)
    trav = BS(webpage.content, "html.parser")
    
    def display_headlines():
        headlines = []
        for link in trav.find_all('a'):
            if str(type(link.string)) == "<class 'bs4.element.NavigableString'>" and len(link.string) > 35:
                headlines.append(link.string)
        
        if headlines:
            for i, headline in enumerate(headlines, 1):
                st.markdown(f"""
                    <p style='font-size: 18px; color: #ffffff; background-color: #2980b9; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>
                        {i}. {headline}
                    </p>
                """, unsafe_allow_html=True)
        else:
            st.write("No headlines found.")
    
    display_headlines()
    
    st.write("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 14px;'>Powered by Business Today | Developed with ❤️ by Sumit Kumar Singh</div>",
        unsafe_allow_html=True
    )

