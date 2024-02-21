import pandas as pd

import streamlit as st
from data_ingestion import connect_db, ingest_data_for_keywords
from utils import read_data

import plotly.graph_objects as go

DATABASE_FILE = 'google_trends_data.db'


def visualize_trends():
    with st.sidebar:
        from_date = st.date_input("Start Date", value=pd.to_datetime("2000-01-01"), max_value=pd.to_datetime("today"))
        to_date = st.date_input("End Date", value=pd.to_datetime("today"))
        keywords = [st.text_input("Keyword 1", key="keyword1")]
        for i in range(2, 5):
            keyword = st.text_input(f"Keyword {i}", key=f"keyword{i}")
            if keyword:
                keywords.append(keyword)
        submitted = st.button('Load Data')

    if submitted and from_date and to_date:
        engine = connect_db(DATABASE_FILE)
        fig = go.Figure()
        for keyword in keywords:
            if keyword:
                with st.spinner(f'Fetching data for {keyword}...'):
                    ingest_data_for_keywords([keyword], from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
                data = read_data(engine, keyword, from_date, to_date)
                if not data.empty:
                    fig.add_trace(go.Scatter(x=data['date'], y=data['value'], mode='lines', name=keyword))
        st.session_state.selected_keywords = keywords
        fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=False)
    else:
        st.error("Please select a date range and at least one keyword.")