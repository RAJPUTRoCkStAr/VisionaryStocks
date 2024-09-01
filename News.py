import streamlit as st
from stocknews import StockNews
import pandas as pd
def news():
    st.title("Stock News and Sentiment Analysis")
    ticker = st.text_input('Enter Stock Ticker').strip().upper()
    if ticker:
        try:
            st.markdown("<div class='section-header'>News</div>", unsafe_allow_html=True)
            sn = StockNews(ticker, save_news=False, wt_key='14c011887083d849610fe8e3a7f848d2')
            df_news = sn.summarize()  
            st.write(f"Type of df_news: {type(df_news)}")
            st.write(df_news) 
            if isinstance(df_news, list):
                for i in range(min(10, len(df_news))):
                    article = df_news[i]
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("<div class='news-item'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='news-title'>{article['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='news-details'><b>Published:</b> {article['published']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='news-details'>{article['summary']}</div>", unsafe_allow_html=True)
                    # st.markdown(f"<div class='news-details'><b>Title Sentiment:</b> {title_sentiment}</div>", unsafe_allow_html=True)
                    # st.markdown(f"<div class='news-details'><b>News Sentiment:</b> {summary_sentiment}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.warning("Could not retrieve news data.")
            st.write(f"Error: {e}")