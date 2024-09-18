for ticker in stocks:
                stock = yf.Ticker(ticker)
                stock_info = pd.DataFrame(stock.info.items(), columns=['Attribute', 'Value'])
                st.write(f"### {ticker}")
                st.dataframe(stock_info)