import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import sqlite3
import matplotlib.pyplot as plt

def port():
    def init_db():
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS portfolio (
                        username TEXT,
                        ticker TEXT,
                        PRIMARY KEY (username, ticker)
                    )''')
        conn.commit()
        conn.close()

    def add_stock(username, ticker):
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO portfolio (username, ticker) VALUES (?, ?)', (username, ticker))
            conn.commit()
            return True  # Stock added successfully
        except sqlite3.IntegrityError:
            return False  # Stock already exists
        finally:
            conn.close()

    def remove_stock(username, ticker):
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        c.execute('DELETE FROM portfolio WHERE username = ? AND ticker = ?', (username, ticker))
        conn.commit()
        conn.close()

    def get_portfolio(username):
        conn = sqlite3.connect('data/database.db')
        c = conn.cursor()
        c.execute('SELECT ticker FROM portfolio WHERE username = ?', (username,))
        stocks = c.fetchall()
        conn.close()
        return [s[0] for s in stocks]

    def fetch_stock_data(ticker):
        data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
        data = data[['Close']]
        return data

    def calculate_bollinger_bands(data, window=20, num_std_dev=2):
        rolling_mean = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        data['BBL'] = rolling_mean - (rolling_std * num_std_dev)
        data['BBM'] = rolling_mean
        data['BBU'] = rolling_mean + (rolling_std * num_std_dev)
        data = data.dropna()
        return data

    def plot_stock_comparison(data1, data2, ticker1, ticker2):
        data1 = calculate_bollinger_bands(data1)
        data2 = calculate_bollinger_bands(data2)
        if data1.empty or data2.empty:
            raise ValueError("Data is empty after cleaning. Check if your input data has enough values.")

        fig, axs = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

        axs[0].plot(data1.index, data1['Close'], label=f'{ticker1} Close Price', color='blue')
        axs[0].plot(data1.index, data1['BBL'], label='Bollinger Lower Band', color='red')
        axs[0].plot(data1.index, data1['BBM'], label='Bollinger Middle Band', color='orange')
        axs[0].plot(data1.index, data1['BBU'], label='Bollinger Upper Band', color='green')
        axs[0].fill_between(data1.index, data1['BBL'], data1['BBU'], color='grey', alpha=0.2)
        axs[0].set_title(f'{ticker1} with Bollinger Bands')
        axs[0].set_ylabel('Price (USD)')
        axs[0].legend()
        axs[0].grid(True)

        axs[1].plot(data2.index, data2['Close'], label=f'{ticker2} Close Price', color='blue')
        axs[1].plot(data2.index, data2['BBL'], label='Bollinger Lower Band', color='red')
        axs[1].plot(data2.index, data2['BBM'], label='Bollinger Middle Band', color='orange')
        axs[1].plot(data2.index, data2['BBU'], label='Bollinger Upper Band', color='green')
        axs[1].fill_between(data2.index, data2['BBL'], data2['BBU'], color='grey', alpha=0.2)
        axs[1].set_title(f'{ticker2} with Bollinger Bands')
        axs[1].set_xlabel('Date')
        axs[1].set_ylabel('Price (USD)')
        axs[1].legend()
        axs[1].grid(True)

        plt.tight_layout()
        return fig

    def display_portfolio(username):
        st.title(f"{username}'s Portfolio")
        stocks = get_portfolio(username)
        if not stocks:
            st.write("Your portfolio is empty.")
        else:
            st.write("### Stocks in your portfolio:")
            st.write(stocks)
            ticker_to_remove = st.selectbox("Select a stock to remove:", stocks)
            if st.button("Remove Stock"):
                remove_stock(username, ticker_to_remove)
                st.success(f"Removed {ticker_to_remove} from your portfolio.")
                st.rerun()

    def add_stock_to_portfolio(username):
        st.title(f"Add Stock to {username}'s Portfolio")
        if 'ticker_input' not in st.session_state:
            st.session_state.ticker_input = ""
        ticker = st.text_input("Enter the stock ticker symbol:", value=st.session_state.ticker_input, key="ticker_input")

        if st.button("Add Stock"):
            if ticker:
                success = add_stock(username, ticker.upper())
                if success:
                    st.success(f"Added {ticker.upper()} to your portfolio.")
                    st.session_state.ticker_input = ""
                else:
                    st.warning(f"The stock {ticker.upper()} is already in your portfolio. Please do not add it again.")
                    # st.session_state.ticker_input = ticker
            st.rerun()

    def compare_stocks(username):
        st.title(f"Compare Stocks in {username}'s Portfolio")
        stocks = get_portfolio(username)
        if len(stocks) < 2:
            st.write("You need at least two stocks in your portfolio to compare.")
            return
        stock1 = st.selectbox("Select the first stock to compare:", stocks)
        stock2 = st.selectbox("Select the second stock to compare:", stocks)
        if st.button("Compare Stocks"):
            if stock1 == stock2:
                st.write("Please select different stocks for comparison.")
            else:
                data1 = fetch_stock_data(stock1)
                data2 = fetch_stock_data(stock2)
                fig = plot_stock_comparison(data1, data2, stock1, stock2)
                st.pyplot(fig)

    # main function logic
    st.sidebar.title("Portfolio Management")
    init_db()
    if "logged_in" in st.session_state and st.session_state.logged_in:
        # Retrieve username from session state
        username = st.session_state.username
        
        menu = st.sidebar.radio("Select an option", ["Add Stock", "View Portfolio", "Compare Stocks"])
        if menu == "Add Stock":
            add_stock_to_portfolio(username)
        elif menu == "View Portfolio":
            display_portfolio(username)
        elif menu == "Compare Stocks":
            compare_stocks(username)
    else:
        st.write("Please log in to access your portfolio.")

 
