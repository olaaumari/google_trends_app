import pandas as pd
import streamlit as st
from data_ingestion import ingest_data_for_keywords
import sqlalchemy
from data_ingestion import connect_db

DATABASE_FILE = 'google_trends_data.db'


def get_connection():
    if 'db_conn' not in st.session_state:
        engine = connect_db(DATABASE_FILE)
        st.session_state['db_conn'] = engine
    return st.session_state['db_conn']


@st.cache_data(hash_funcs={sqlalchemy.engine.base.Engine: id})
def read_data(engine, keyword, from_date, to_date):
    """
    Lit les données de la base pour un mot-clé spécifique et une plage de dates.
    """
    query = f"""
    SELECT date, value 
    FROM google_trends_data 
    WHERE keyword = '{keyword}' 
    AND date BETWEEN '{from_date}' AND '{to_date}'
    """
    with engine.connect() as connection:
        data = pd.read_sql(query, con=connection)
    if not data.empty:
        data['date'] = pd.to_datetime(data['date'])
        
    return data.drop_duplicates(subset=['date'], keep='first')

def ensure_data_for_keyword(engine, keyword, from_date, to_date):
    """
    S'assure que les données pour le mot-clé donné existent pour la plage de dates.
    Si non, récupère les données depuis Google Trends et les insère dans la base de données.
    """
    data = read_data(engine, keyword, from_date, to_date)
    if data.empty:
        # Les données pour ce mot-clé et cette plage de dates n'existent pas
        # Récupérer et insérer les données
        ingest_data_for_keywords([keyword], from_date, to_date)
        data = read_data(engine, keyword, from_date, to_date)  # Relire les données
    return data