import pandas as pd

from data_ingestion import ingest_data_for_keywords

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
    return data

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