import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


from functions import create_podium, display_comparative_stats, create_pie_chart, calculate_participation_2022, historical_data, create_scatter_plot, create_histograms
def resultats_cles(df_tour1_processed, df_tour2_processed) : 
    
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
                Résultats Clé
        </h1>
        <hr style='
                border: 0;
                height: 2px;
                background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
                margin: 30px 0;
        '>
        """,unsafe_allow_html=True)

    
    display_comparative_stats(df_tour1_processed, df_tour2_processed)
    
    
    # Calcul des taux de 2022
    participation_2022_1 = calculate_participation_2022(df_tour1_processed)
    participation_2022_2 = calculate_participation_2022(df_tour2_processed)

    # Ajout des données de 2022
    historical_data['2022'] = [participation_2022_1, participation_2022_2]

    # Création du graphique
    fig, ax = plt.subplots(figsize=(12, 6))

    years = list(historical_data.keys())
    x = range(len(years))
    width = 0.35

    tour1 = [data[0] for data in historical_data.values()]
    tour2 = [data[1] for data in historical_data.values()]

    ax.bar([i - width/2 for i in x], tour1, width, label='1er Tour', color='#3498db')
    ax.bar([i + width/2 for i in x], tour2, width, label='2ème Tour', color='#e74c3c')

    ax.set_ylabel('Taux de participation (%)')
    ax.set_title('Taux de participation aux élections présidentielles françaises (2002-2022)')
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend()

    # Ajout des valeurs sur les barres
    for i, v in enumerate(tour1):
        ax.text(i - width/2, v, f'{v:.2f}%', ha='center', va='bottom')
    for i, v in enumerate(tour2):
        ax.text(i + width/2, v, f'{v:.2f}%', ha='center', va='bottom')

    ax.set_ylim(0, 100)  # Échelle de 0 à 100%

    # Affichage dans Streamlit
    st.pyplot(fig)
#############################################################################################################################################    
    
    st.markdown(f"""
        <br><br>
        <hr style='
                border: 0;
                height: 2px;
                background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
                margin: 30px 0;
        '>
        <br>
        """,unsafe_allow_html=True)

    
    
    create_podium(df_tour1_processed, "Résultats du 1er Tour", "Par rapport aux voix exprimées", "exp")
    create_podium(df_tour2_processed, "Résultats du 2ème Tour", "Par rapport aux voix exprimées", "exp")
    create_podium(df_tour1_processed, "Résultats du 1er Tour", "Par rapport aux inscrits", "ins")
    create_podium(df_tour2_processed, "Résultats du 2ème Tour", "Par rapport aux inscrits", "ins")
    
#############################################################################################################################################    

    st.markdown(f"""
        <br><br>
        <hr style='
                border: 0;
                height: 2px;
                background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
                margin: 30px 0;
        '>
        <br>
        """,unsafe_allow_html=True)

    
        # Création et affichage des graphiques
    st.markdown("## Résultats des élections présidentielles par candidat")

    # Graphique pour le premier tour
    fig1 = create_pie_chart(df_tour1_processed, "1er Tour")
    st.pyplot(fig1)

    # Graphique pour le second tour
    fig2 = create_pie_chart(df_tour2_processed, "2ème Tour")
    st.pyplot(fig2)
    
    
    #############################################################################################################################################    

        
    # Création et affichage des graphiques
    st.markdown("## Relation entre Taux de Participation et Score du Gagnant par Département")

    # Graphique pour le premier tour
    fig1 = create_scatter_plot(df_tour1_processed, "1er Tour")
    st.pyplot(fig1)

    # Graphique pour le second tour
    fig2 = create_scatter_plot(df_tour2_processed, "2ème Tour")
    st.pyplot(fig2)

    st.markdown("""
    ### Interprétation :
    - Chaque point représente un département.
    - La couleur indique le candidat gagnant dans ce département.
    - La taille du point est proportionnelle au nombre d'inscrits dans le département.
    - La ligne rouge en pointillés représente la tendance générale (régression linéaire).
    """)
    
    
#####################################################################################################################################

    # Création et affichage des histogrammes
    st.markdown("## Distribution des Taux de Participation et des Scores des Candidats")

    # Histogrammes pour le premier tour
    st.markdown("### Premier Tour")
    create_histograms(df_tour1_processed, "1er Tour")

    # Histogrammes pour le second tour
    st.markdown("### Second Tour")
    create_histograms(df_tour2_processed, "2ème Tour")

    # Ajouter une interprétation
    st.markdown("""
    ### Interprétation :
    - L'histogramme du taux de participation montre comment les taux varient entre les départements.
    - Les histogrammes des scores des candidats montrent la distribution de leurs performances à travers les départements.
    - Une distribution étalée indique une grande variabilité entre les départements.
    - Une distribution resserrée suggère des performances plus uniformes à travers le pays.
    - Observez les différences entre le premier et le second tour, notamment pour les candidats qualifiés.
    """)