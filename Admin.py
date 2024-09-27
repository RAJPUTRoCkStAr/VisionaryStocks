import sqlite3
import pandas as pd
import streamlit as st
def view_database():
    database_path = 'Data/database.db'
    st.markdown(f"<h1 style='text-align: center;color:white'>Database Viewer</h1>", unsafe_allow_html=True)
    if st.session_state['authenticated']:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        tables = [table[0] for table in tables]
        if tables:
            table_selection = st.selectbox("select", tables,label_visibility="hidden")
            if table_selection:
                conn = sqlite3.connect(database_path)
                df = pd.read_sql_query(f'SELECT * FROM {table_selection}', conn)
                conn.close()
                st.markdown(f"<h2 style='text-align: center;color:white'>Viewing  {table_selection.capitalize()} Database 📝</h2>", unsafe_allow_html=True)
                st.dataframe(df,use_container_width=True,hide_index=True)
        else:
            st.write("No tables found in the database.")
    if st.button('Log Out'):
        st.session_state.log_in = False
        st.session_state.pag = "Home"
        st.rerun()