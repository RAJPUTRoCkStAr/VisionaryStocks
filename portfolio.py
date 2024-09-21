import streamlit as st
import pandas as pd
import yfinance as yf
import sqlite3
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu

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
    # Assuming calculate_bollinger_bands is already defined
        data1 = calculate_bollinger_bands(data1)
        data2 = calculate_bollinger_bands(data2)

        if data1.empty or data2.empty:
            raise ValueError("Data is empty after cleaning. Check if your input data has enough values.")

        # Create subplots: one row, two plots
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=[f'{ticker1} with Bollinger Bands', f'{ticker2} with Bollinger Bands'])

        # First stock plot (ticker1)
        fig.add_trace(go.Scatter(x=data1.index, y=data1['Close'], mode='lines', name=f'{ticker1} Close Price', line=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=data1.index, y=data1['BBL'], mode='lines', name='Bollinger Lower Band', line=dict(color='red')), row=1, col=1)
        fig.add_trace(go.Scatter(x=data1.index, y=data1['BBM'], mode='lines', name='Bollinger Middle Band', line=dict(color='orange')), row=1, col=1)
        fig.add_trace(go.Scatter(x=data1.index, y=data1['BBU'], mode='lines', name='Bollinger Upper Band', line=dict(color='green')), row=1, col=1)

        # Add shaded area between Bollinger Bands for stock 1
        fig.add_trace(go.Scatter(x=data1.index, y=data1['BBU'], fill='tonexty', fillcolor='rgba(128, 128, 128, 0.2)', line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=data1.index, y=data1['BBL'], fill='none', line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=1, col=1)

        # Second stock plot (ticker2)
        fig.add_trace(go.Scatter(x=data2.index, y=data2['Close'], mode='lines', name=f'{ticker2} Close Price', line=dict(color='blue')), row=2, col=1)
        fig.add_trace(go.Scatter(x=data2.index, y=data2['BBL'], mode='lines', name='Bollinger Lower Band', line=dict(color='red')), row=2, col=1)
        fig.add_trace(go.Scatter(x=data2.index, y=data2['BBM'], mode='lines', name='Bollinger Middle Band', line=dict(color='orange')), row=2, col=1)
        fig.add_trace(go.Scatter(x=data2.index, y=data2['BBU'], mode='lines', name='Bollinger Upper Band', line=dict(color='green')), row=2, col=1)

        # Add shaded area between Bollinger Bands for stock 2
        fig.add_trace(go.Scatter(x=data2.index, y=data2['BBU'], fill='tonexty', fillcolor='rgba(128, 128, 128, 0.2)', line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=data2.index, y=data2['BBL'], fill='none', line=dict(color='rgba(255,255,255,0)'), showlegend=False), row=2, col=1)

        # Update layout to include title and axis labels
        fig.update_layout(
            title=f'Comparison of {ticker1} and {ticker2} with Bollinger Bands',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            legend_title='Indicators',
            height=800
        )

        # Update axes titles for individual subplots
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
        fig.update_yaxes(title_text="Price (USD)", row=2, col=1)

        return fig

    def display_portfolio(username):
            stocks = get_portfolio(username)

            if not stocks:
                st.markdown("<h3 style='text-align: center; color: red;'>Your portfolio is empty.</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h4 style='text-align: center; color: #4CAF50;'>Stocks in Your Portfolio</h4>", unsafe_allow_html=True)

                for ticker in stocks:
                    # Get stock info and history
                    stock = yf.Ticker(ticker)
                    stock_data = stock.history(period="5y")

                    # Stock ticker as a header
                    st.markdown(f"<h2 style='text-align: center; color: #1976D2;'>{ticker.upper()}</h2>", unsafe_allow_html=True)

                    # Create columns for layout
                    stock_info_col, chart_col = st.columns([1, 3])

                    # Stock Information
                    with stock_info_col:
                        stock = yf.Ticker(ticker)
                        stock_info = pd.DataFrame(stock.info.items(), columns=['Attribute', 'Value'])
                        st.dataframe(stock_info,use_container_width=True,hide_index=True)
                    # Stock Price Chart using Plotly
                    with chart_col:
                        # Create interactive plot using Plotly
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'],
                                                 mode='lines', name='Close Price', line=dict(color='#FF5722')))
                        fig.update_layout(
                            title=f'{ticker.upper()} - 5 Year Performance',
                            xaxis_title='Date',
                            yaxis_title='Price (USD)',
                            plot_bgcolor='#0E1117',
                            paper_bgcolor='#0E1117',
                            font=dict(color='white'),
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig)

                    # Display other financials in expandable sections
                    with st.expander(f"More Details for {ticker.upper()}"):
                        st.markdown("### Financial Data")
                        financials = stock.financials.T  # Transpose for readability
                        st.dataframe(financials.style.format("{:,.2f}").background_gradient(cmap="Blues"))

                        st.markdown("### Balance Sheet")
                        balance_sheet = stock.balance_sheet.T  # Transpose for readability
                        st.dataframe(balance_sheet.style.format("{:,.2f}").background_gradient(cmap="Greens"))


                        st.markdown("### Dividends & Splits")
                        dividends = stock.dividends
                        if dividends.empty:
                            st.write("No dividends data available.")
                        else:
                            st.dataframe(dividends, height=150)

                        splits = stock.splits
                        if splits.empty:
                            st.write("No stock split data available.")
                        else:
                            st.dataframe(splits, height=150)

                # Option to remove stock
                ticker_to_remove = st.selectbox("Select a stock to remove:", stocks, key="remove_stock")
                if st.button("Remove Stock"):
                    remove_stock(username, ticker_to_remove)
                    st.success(f"✅ Removed {ticker_to_remove} from your portfolio.")
                    st.experimental_rerun()

    def add_stock_to_portfolio(username):
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
    def format_large_number(num):
        """Converts large numbers into a more readable format with words."""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f} Billion"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.2f} Million"
        elif num >= 1_000:
            return f"{num / 1_000:.2f} Thousand"
        else:
            return f"{num:,}"
    def compare_stocks(username):
        stocks = get_portfolio(username)

        if len(stocks) < 2:
            st.write("You need at least two stocks in your portfolio to compare.")
            return

        stock1_ticker = st.selectbox("Select the first stock to compare:", stocks)
        stock2_ticker = st.selectbox("Select the second stock to compare:", stocks)

        if st.button("Compare Stocks"):
            if stock1_ticker == stock2_ticker:
                st.write("Please select different stocks for comparison.")
            else:
                stock1 = yf.Ticker(stock1_ticker)
                stock2 = yf.Ticker(stock2_ticker)

                data1 = fetch_stock_data(stock1_ticker)
                data2 = fetch_stock_data(stock2_ticker)
                fig = plot_stock_comparison(data1, data2, stock1_ticker, stock2_ticker)
                st.plotly_chart(fig)

                # Extracting financial information
                apple_pe_ratio = stock1.info.get('trailingPE', 'N/A')
                microsoft_pe_ratio = stock2.info.get('trailingPE', 'N/A')
                apple_eps = stock1.info.get('trailingEps', 'N/A')
                microsoft_eps = stock2.info.get('trailingEps', 'N/A')
                apple_dividend = stock1.info.get('dividendYield', 'N/A')
                microsoft_dividend = stock2.info.get('dividendYield', 'N/A')
                apple_revenue = stock1.info.get('totalRevenue', 'N/A')
                microsoft_revenue = stock2.info.get('totalRevenue', 'N/A')

                # Using two columns to display side-by-side comparison
                col1, col2 = st.columns(2)

                # Column 1 for Stock 1 (Apple)
                with col1:
                    st.markdown(f"<h2 style='text-align: center;'>{stock1_ticker} 📈</h2>", unsafe_allow_html=True)
                    st.markdown(f"**P/E Ratio:** {apple_pe_ratio}")
                    st.markdown(f"**EPS:** {apple_eps}")
                    st.markdown(f"**Dividend Yield:** {apple_dividend * 100 if apple_dividend != 'N/A' else 'N/A'}%")
                    st.markdown(f"**Revenue:** ${format_large_number(apple_revenue)} USD" if apple_revenue != 'N/A' else "**Revenue:** N/A")

                # Column 2 for Stock 2 (Microsoft)
                with col2:
                    st.markdown(f"<h2 style='text-align: center;'>{stock2_ticker} 📉</h2>", unsafe_allow_html=True)
                    st.markdown(f"**P/E Ratio:** {microsoft_pe_ratio}")
                    st.markdown(f"**EPS:** {microsoft_eps}")
                    st.markdown(f"**Dividend Yield:** {microsoft_dividend * 100 if microsoft_dividend != 'N/A' else 'N/A'}%")
                    st.markdown(f"**Revenue:** ${format_large_number(microsoft_revenue)} USD" if microsoft_revenue != 'N/A' else "**Revenue:** N/A")

                st.markdown("""
                    <style>
                    h2 {
                        color: #0073e6;
                    }
                    .stMarkdown {
                        font-size: 16px;
                        font-weight: bold;
                    }
                    </style>
                """, unsafe_allow_html=True)
    
    init_db()
    if "logged_in" in st.session_state and st.session_state.logged_in:
        username = st.session_state.username.capitalize()
        
        menu = option_menu(None, 
                           options = ["Add Stock", "View Portfolio", "Compare Stocks"],icons=['plus-circle-fill', 'briefcase-fill', 'bar-chart-line-fill'],orientation='horizontal')
        if menu == "Add Stock":
            add_stock_to_portfolio(username)
        elif menu == "View Portfolio":
            display_portfolio(username) 
        elif menu == "Compare Stocks":
            compare_stocks(username)
    else:
        st.write("Please log in to access your portfolio.")

 
