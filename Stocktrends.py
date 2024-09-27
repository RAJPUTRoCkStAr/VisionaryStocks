import streamlit as st
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from yahooquery import search
import pandas as pd
from streamlit_option_menu import option_menu
import time
def fetch_gainers():
    url = 'https://www.nseindia.com/api/live-analysis-variations?index=gainers'
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nseindia.com/"
    }
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json().get('legends', [])
            selected_legend = option_menu(None, [legend[0] for legend in data],orientation='horizontal',icons=None)
            if selected_legend:
                table = [{
                    "Symbol": item['symbol'],
                    "Open Price": f"{item['open_price']:.2f}",
                    "High Price": f"{item['high_price']:.2f}",
                    "Low Price": f"{item['low_price']:.2f}",
                    "Previous Price": f"{item['prev_price']:.2f}",
                    "Change (%)": f"{item['perChange']:.2f}"
                } for item in response.json()[selected_legend]["data"]]
                display_cards(pd.DataFrame(table))
        except requests.exceptions.JSONDecodeError:
            st.error("Failed to parse JSON.")
    else:
        st.error(f"Failed to retrieve data. Status code: {response.status_code}")
def display_cards(df):
    num_cols = 4  
    num_rows = (len(df) + num_cols - 1) // num_cols  

    for row_idx in range(num_rows):
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            card_idx = row_idx * num_cols + col_idx
            if card_idx < len(df):
                row = df.iloc[card_idx]
                cols[col_idx].markdown(f"""
                    <div style="border-radius: 8px; padding: 16px; margin: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                        <h4 style="margin: 0;color:#f09707">{row['Symbol']}</h4>
                        <h5 style="color:yellow;"><strong>Open Price:</strong> {row['Open Price']}</h5>
                        <h5 style="color:#07f00b;"><strong>High Price:</strong> {row['High Price']}</h5>
                        <h5 style="color:red;"><strong>Low Price:</strong> {row['Low Price']}</h5>
                        <h5 style="color:#07b6f0;"><strong>Previous Close:</strong> {row['Previous Price']}</h5>
                        <h5 style="color:#b207f0;"><strong>Change (%):</strong> {row['Change (%)']}</h5>
                    </div>
                """, unsafe_allow_html=True)

def scrape_top_losers():
    url = "https://groww.in/markets/top-losers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table')
    if not table:
        return []
    
    headers = [header.get_text() for header in table.find_all('th')]
    rows = [
        dict(zip(headers, [col.get_text(strip=True) for col in row.find_all('td')]))
        for row in table.find_all('tr')[1:] if row.find_all('td')
    ]
    return rows


def get_tickers_from_names(companies):
    tickers = {}
    for company in companies:
        try:
            results = search(company).get('quotes', [])
            tickers[company] = results[0]['symbol'] if results else None
        except Exception:
            tickers[company] = None
    return tickers


def fetch_stock_data(tickers):
    data = {}
    for company, symbol in tickers.items():
        if not symbol:
            data[company] = {key: None for key in ['Open Price', 'High Price', 'Low Price', 'Previous Close', 'Close', 'Change (%)']}
            continue
        
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='5d')
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                curr_close = hist['Close'].iloc[-1]
                change = curr_close - prev_close
                data[company] = {
                    'Open Price': hist['Open'].iloc[-1],
                    'High Price': hist['High'].iloc[-1],
                    'Low Price': hist['Low'].iloc[-1],
                    'Previous Close': prev_close,
                    'Close': curr_close,
                    'Change (%)': (change / prev_close) * 100
                }
            else:
                data[company] = {key: None for key in ['Open Price', 'High Price', 'Low Price', 'Previous Close', 'Close', 'Change (%)']}
        except Exception as e:
            st.error(f"Error fetching data for {company}: {e}")
            data[company] = {key: None for key in ['Open Price', 'High Price', 'Low Price', 'Previous Close', 'Close', 'Change (%)']}
    
    return data


def fetch_indices(indices):
    index_data = {}
    for name, ticker in indices.items():
        try:
            index = yf.Ticker(ticker)
            data = index.history(period="5d")
            if len(data) < 2:
                index_data[name] = {'close': None, 'change': None, 'percent_change': None}
                continue

            previous_close = data['Close'].iloc[-2]
            current_close = data['Close'].iloc[-1]
            change = current_close - previous_close
            percent_change = (change / previous_close) * 100

            index_data[name] = {
                'close': current_close,
                'change': change,
                'percent_change': percent_change
            }
        except Exception as e:
            st.error(f"Error fetching data for {name}: {e}")
            index_data[name] = {'close': None, 'change': None, 'percent_change': None}
    
    return index_data


def display_losers():
    st.header("Top Losers")
    with st.spinner('Getting your data...🤖'):
        data = scrape_top_losers()
        if data:
            companies = [item['Company'] for item in data]
            tickers = get_tickers_from_names(companies)
            stock_data = fetch_stock_data(tickers)
            df = pd.DataFrame(stock_data).T.reset_index()
            df.columns = ['Company', 'Open Price', 'High Price', 'Low Price', 'Previous Price', 'Close', 'Change (%)']
            df.rename(columns={'Company': 'Symbol'}, inplace=True)
            st.write("### Top Losers Data")
            display_ca(df)
        else:
            st.write('No data found or unable to fetch data.')


def display_ca(df):
    num_cols = 4  
    num_rows = (len(df) + num_cols - 1) // num_cols  

    for row_idx in range(num_rows):
        cols = st.columns(num_cols)
        for col_idx in range(num_cols):
            card_idx = row_idx * num_cols + col_idx
            if card_idx < len(df):
                row = df.iloc[card_idx]
                cols[col_idx].markdown(f"""
                    <div style="border-radius: 8px; padding: 16px; margin: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                        <h4 style="margin: 0;">{row['Symbol']}</h4>
                        <p style="color:yellow"><strong>Open Price:</strong> {row['Open Price']}</p>
                        <p style="color:#07f00b"><strong>High Price:</strong> {row['High Price']}</p>
                        <p style="color:red"><strong>Low Price:</strong> {row['Low Price']}</p>
                        <p style="color:orange"><strong>Previous Close:</strong> {row['Previous Price']}</p>
                        <p style="color:#07b6f0"><strong>Close:</strong> {row['Close']}</p>
                        <p style="color:#b207f0"><strong>Change (%):</strong> {row['Change (%)']}</p>
                    </div>
                """, unsafe_allow_html=True)


def display_indices():
    indices = {
        "Nifty 50": "^NSEI", "Nifty Bank": "^NSEBANK", "Sensex": "^BSESN",
        "Finnifty": "NIFTY_FIN_SERVICE.NS", "Nifty 100": "^CNX100", 
        "S&P 500": "^GSPC", "Dow Jones": "^DJI"
    }
    
    st.markdown("<div class='custom-header'>Real-Time Indices Data</div>", unsafe_allow_html=True)
    placeholder = st.empty()
    
    while True:
        data = fetch_indices(indices)
        with placeholder.container():
            display_car(data, 'indices')
        time.sleep(1)
def display_car(data, data_type):
        cols = st.columns(4)
        for i, (name, stats) in enumerate(data.items()):
            cols[i % 4].metric(
                label=name,
                value=f"{stats['close']:.2f}" if stats['close'] else "N/A",
                delta=f"{stats['change']:.2f} ({stats['percent_change']:.2f}%)" if stats['change'] else "N/A"
            )

def Stocktre():
    st.title("")
    st.markdown(f"<h1 style='text-align: center;color:#ff4b4b;'>Stock Market Trends</h1>", unsafe_allow_html=True)

    app = option_menu(None,options=['Gainers','Loosers','Indices'],icons=['graph-up-arrow','graph-down-arrow','pie-chart'],orientation='horizontal')
    if app == 'Gainers':
        fetch_gainers()
    elif app == 'Loosers':
        display_losers()
    elif app == 'Indices':
        display_indices()


