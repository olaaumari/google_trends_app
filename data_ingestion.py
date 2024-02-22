from pytrends.request import TrendReq
import pandas as pd
from sqlalchemy import create_engine, text
import datetime

# Chemin par défaut de la base de données SQLite
DATABASE_FILE = 'google_trends_data.db'

def connect_db(file_path=DATABASE_FILE):
    """
    Établir une connexion à la base de données SQLite spécifiée.

    Parameters:
    - file_path (str): Chemin vers le fichier de base de données SQLite. Par défaut, 'google_trends_data.db'.

    Returns:
    - engine: Instance de connexion à la base de données.
    """
    engine = create_engine(f'sqlite:///{file_path}')
    return engine


def get_google_trends_data(keyword, from_date, to_date):
    """
    Récupère les données de tendance Google pour un mot-clé donné sur une période spécifiée.

    Parameters:
    - keyword (str): Le mot-clé pour lequel récupérer les données de tendance.
    - from_date (str): La date de début de la période de tendance (format 'YYYY-MM-DD').
    - to_date (str): La date de fin de la période de tendance (format 'YYYY-MM-DD').

    Returns:
    - df (DataFrame): Un DataFrame pandas contenant les données de tendance pour le mot-clé.
    """
    pytrend = TrendReq(hl='fr-FR')
    pytrend.build_payload([keyword], timeframe=f'{from_date} {to_date}')
    df = pytrend.interest_over_time()
    if not df.empty:
        df = df.drop(labels=['isPartial'], axis='columns', errors='ignore')
        df.rename(columns={keyword: 'value'}, inplace=True)
        df['keyword'] = keyword  
        df.reset_index(inplace=True)
    return df

def create_table(engine):
    """
    Crée une table dans la base de données pour stocker les données de tendance Google, si elle n'existe pas déjà.

    Parameters:
    - engine: L'instance de connexion à la base de données.
    """
    create_table_query = text("""
    CREATE TABLE IF NOT EXISTS google_trends_data (
        date DATE,
        keyword VARCHAR(255),
        value INTEGER,
        PRIMARY KEY (date, keyword)
    );
    """)
    with engine.connect() as connection:
        connection.execute(create_table_query)


def insert_data(engine, data):
    """
    Insère les données de tendance dans la base de données.

    Parameters:
    - engine: L'instance de connexion à la base de données.
    - data (DataFrame): Les données de tendance à insérer.
    """
    if not data.empty:
        data.to_sql('google_trends_data', con=engine, if_exists='append', index=False, method='multi')


def ingest_data_for_keywords(keywords, from_date, to_date):
    """
    Ingeste les données de tendance Google pour une liste de mots-clés sur une période donnée.

    Parameters:
    - keywords (list of str): Liste des mots-clés pour lesquels récupérer les données.
    - from_date (str): La date de début de la période de tendance.
    - to_date (str): La date de fin de la période de tendance.
    """
    engine = connect_db()
    create_table(engine)

    for keyword in keywords:
        data = get_google_trends_data(keyword, from_date, to_date)
        if not data.empty:
            insert_data(engine, data)


if __name__ == "__main__":
    keywords = ['Niska']  # Exemple avec un seul mot-clé, mais peut être une liste de plusieurs mots-clés
    today = datetime.date.today()
    three_months_ago = today - datetime.timedelta(days=90)
    from_date = three_months_ago.strftime('%Y-%m-%d')
    to_date = today.strftime('%Y-%m-%d')
    print(to_date)
    ingest_data_for_keywords(keywords, from_date, to_date)
