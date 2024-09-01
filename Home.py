import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from lotti import lottie_company,lottie_hello,lottie_me
def home():
    st.header("Stock Price Prediction", divider='rainbow')
    hello = st_lottie(lottie_hello, speed=1, reverse=True, loop=True, quality='medium', height=180, width=180, key=None)
    col1, col2 = st.columns(2)

    with col1:
        st.header("Purpose of the App")
        st.write("This abstract delves into the critical realm of stock price prediction within financial markets. It underscores the utilization of historical data, mathematical frameworks, and machine learning methodologies to anticipate forthcoming movements in stock prices. By scrutinizing factors like market trends, company performance, economic indices, and investor sentiment, predictive models aim to offer insights into potential price shifts. The significance of precise predictions for investors, traders, and financial institutions is emphasized, along with the inherent challenges and complexities in this endeavor. Continuous refinement of algorithms and integration of new data sources are highlighted as avenues to bolster the accuracy and dependability of stock price prediction models. Ultimately, these efforts contribute to informed decision-making within the dynamic landscape of finance.")

    with col2:
        lottie_company
        comapny = st_lottie(lottie_company, speed=1, reverse=True, loop=True, quality='medium', height=None, width=None, key=None)

    tab = option_menu(None, ["Overview 🗒️", "Future Enhancements 📈"], orientation="horizontal")

    if tab == "Overview 🗒️":
        st.subheader("Overview 🗒️ & Key Features:")
        st.markdown("Interactive Map Integration: Users can easily locate companies by country or city, providing geographical context to the stock prediction process.")
        st.markdown("Industry Selection: Users can specify the industry they are interested in, refining their search and predictions based on sector-specific data.")
        st.markdown("Comprehensive Company Database: The platform offers a vast database of companies, ensuring users have access to a wide range of options for stock price prediction.")
        st.markdown("Up-to-Date Data: The platform constantly updates its data to provide users with the latest information, enabling accurate and timely predictions")
        st.markdown("User-Friendly Interface: The interface is designed to be intuitive and user-friendly, allowing users to navigate the platform effortlessly and access the information they need quickly.")
        st.markdown("Advanced Prediction Algorithms: Utilizing cutting-edge machine learning and statistical techniques, the platform generates reliable predictions based on historical data and market trends.")

    elif tab == "Future Enhancements 📈":  
        st.subheader("Future Enhancements: 📈")
        st.markdown("Deep Learning Integration: Incorporate deep learning models, such as recurrent neural networks (RNNs) or transformers, to capture intricate patterns in historical stock data, potentially improving prediction accuracy and robustness.")
        st.markdown("Explainable AI (XAI): Implement explainable AI techniques to provide users with insights into the factors driving stock price predictions, enhancing transparency and trust in the platform's recommendations.")
        st.markdown("Scenario Analysis Tools: Develop tools for scenario analysis, allowing users to simulate the impact of various economic, geopolitical, or industry-specific events on stock prices and portfolio performance.")
        st.markdown("Quantum Computing Integration: Explore the integration of quantum computing algorithms to tackle complex optimization problems inherent in portfolio management and risk assessment, potentially unlocking new levels of performance and efficiency.")
        st.markdown("Dynamic Risk Management Tools: Introduce dynamic risk management tools that adapt to changing market conditions and user preferences, enabling users to adjust risk levels and portfolio allocations in real time.")
        st.markdown("Robo-Advisory Services: Integrate robo-advisory services powered by AI algorithms, offering users personalized investment recommendations based on their financial goals, risk tolerance, and investment horizon.")
        st.markdown("Customizable Machine Learning Pipelines: Empower users to customize machine learning pipelines by selecting from a range of algorithms, feature engineering techniques, and hyperparameters, catering to individual preferences and requirements.")
        st.markdown("Social Sentiment Analysis: Enhance sentiment analysis capabilities by incorporating social media data from platforms like Twitter, Reddit, and StockTwits, providing users with real-time insights into market sentiment and investor behavior.")
        st.write("Stay tuned for these transformative updates!")


            

    st.write("⭐ Feel free to explore the app and stay tuned for future updates!")

