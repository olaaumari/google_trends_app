import streamlit as st
import pandas as pd

# Chemin de la base de données SQLite
DATABASE_FILE = 'google_trends_data.db'


from page_01_visualisation import visualize_trends


# Prochainement 
# def model_training():
#     st.write("Model Training Section")
#     from_date = st.date_input("Start Date for Model", value=pd.to_datetime("2023-01-01"), key='model_start_date')
#     to_date = st.date_input("End Date for Model", value=pd.to_datetime("today"), key='model_end_date')
            
#     # Utiliser les mots-clés sélectionnés par l'utilisateur
#     keywords = st.session_state.get('selected_keywords', [])
    
#     for keyword in keywords:
#         st.subheader(f"Features for {keyword}")
        
#         # Importez votre script de feature engineering
#         data_with_features = process_keyword_series(keyword, from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'))
        
#         if not data_with_features.empty:
#             st.dataframe(data_with_features)
#         else:
#             st.write(f"No data available for {keyword} within the selected dates.")


def main():
    st.title('Google Trends Data Visualization and Model Training')
    
    tab1, tab2 = st.tabs(["Trends Visualization", "Model Training"])
    
    with tab1:
        visualize_trends()
    
    #with tab2:
    #    model_training()

if __name__ == "__main__":
    main()
