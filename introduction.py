import streamlit as st
import matplotlib.pyplot as plt
import missingno as msno
import io
import pandas as pd
import altair as alt

from functions import create_columns_html


def introduction(df1, df1_processed, df2, df2_processed):
    
    
    #DataFrame 1
    
    
    st.markdown(f"""
    <h1 style='
            text-align: center; 
            color: #1E1E1E;
            margin-bottom: 20px;
            margin-top: 20px;
            font-size: 48px;
            font-family: Arial, sans-serif;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            letter-spacing: 1px;
        '>
            Présentation du Dataset
    </h1>
    <hr style='
            border: 0;
            height: 2px;
            background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
            margin: 30px 0;
    '>
    """,unsafe_allow_html=True)
    

    
    st.markdown("""
        <h3 style='text-align: center;'>Dimensions Du Dataset - Tour 1</h3>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <p style='text-align: center;'>Nombre de lignes: {df1.shape[0]}</p>
        <p style='text-align: center;'>Nombre de colonnes: {df1.shape[1]}</p>
    """, unsafe_allow_html=True)
    
    # Obtenir les noms des colonnes
    column_names = df1.columns.tolist()
    column_names_processed = df1_processed.columns.tolist()

    # Créer le HTML pour afficher les noms des colonnes du premier DataFrame
    columns_html = create_columns_html(column_names, 7)

    # Créer le HTML pour afficher les noms des colonnes du DataFrame traité
    columns_html_processed1 = create_columns_html(column_names_processed[:21], 7)
    columns_html_processed2 = create_columns_html(column_names_processed[21:], 4)

    
    plt.figure(figsize=(14, 7))  # Ajuster selon le besoin
    msno.matrix(df1_processed)
    
    # Sauvegarder le graphique dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Convertir l'image en base64 pour l'affichage HTML
    import base64
    img_str = base64.b64encode(buf.getvalue()).decode()
    
    # Fermer la figure pour libérer la mémoire
    plt.close()


    # Utilisez st.markdown pour afficher le HTML
    st.markdown(f"""
    <center>
    <h3>Noms des Colonnes du Dataset Brute - Tour 1</h3>
    {columns_html}
    <h3>Noms des Colonnes Modifiés</h3>
    {columns_html_processed1}
    <p></p>
    {columns_html_processed2}
    <p></p>
    <p></p>
    <h3>Matrice des Valeurs Manquantes</h3>
    <img src="data:image/png;base64,{img_str}" alt="Missing Values Matrix">
    </center>
    """, unsafe_allow_html=True)
    
    
    st.markdown(f"""
    <center>
    <h3>Description</h3>
                """,unsafe_allow_html=True)
    
    df1_describe = df1_processed.describe()
    st.dataframe(df1_describe)

        #DataFrame 2
    
    st.markdown(f"""
    <center>
    <p></p>
    <p></p>
    <p></p>
    """,unsafe_allow_html=True)
    
    
    st.markdown(
        """
        <hr style='
            border: 0;
            height: 2px;
            background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
            margin: 30px 0;
        '>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("""
        <h3 style='text-align: center;'>Dimensions Du Dataset - Tour 2</h3>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <p style='text-align: center;'>Nombre de lignes: {df2.shape[0]}</p>
        <p style='text-align: center;'>Nombre de colonnes: {df2.shape[1]}</p>
    """, unsafe_allow_html=True)
    
    # Obtenir les noms des colonnes
    column_names_t2 = df2.columns.tolist()
    column_names_processed_t2 = df2_processed.columns.tolist()

    # Créer le HTML pour afficher les noms des colonnes du premier DataFrame
    columns_html_t2 = create_columns_html(column_names_t2, 7)
    
    # Créer le HTML pour afficher les noms des colonnes du DataFrame traité
    columns_html_processed1_t2 = create_columns_html(column_names_processed_t2[:21], 7)
    columns_html_processed2_t2 = create_columns_html(column_names_processed_t2[21:], 4)
    
    plt.figure(figsize=(14, 7))  # Ajuster selon le besoin
    msno.matrix(df2_processed)
    
    # Sauvegarder le graphique dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Convertir l'image en base64 pour l'affichage HTML
    import base64
    img_str = base64.b64encode(buf.getvalue()).decode()
    
    # Fermer la figure pour libérer la mémoire
    plt.close()


    # Utilisez st.markdown pour afficher le HTML
    st.markdown(f"""
    <center>
    <h3>Noms des Colonnes du Dataset Brute - Tour 2</h3>
    {columns_html_t2}
    <h3>Noms des Colonnes Modifiés</h3>
    {columns_html_processed1_t2}
    <p></p>
    {columns_html_processed2_t2}
    <p></p>
    <p></p>
    <h3>Matrice des Valeurs Manquantes</h3>
    <img src="data:image/png;base64,{img_str}" alt="Missing Values Matrix">
    </center>
    """, unsafe_allow_html=True)
    
    
    st.markdown(f"""
    <center>
    <h3>Description</h3>
                """,unsafe_allow_html=True)
    
    df2_describe = df2_processed.describe()
    st.dataframe(df2_describe)