import streamlit as st
from functions import informations_heatmaps, custom_mapping, create_france_winner_map, candidate_score_heatmaps

def maps(df_processed, df_processed2):
    st.markdown(
        """
        <h1 style='text-align: center; color: #1E1E1E; margin-bottom: 20px; margin-top: 20px; font-size: 48px; font-family: Arial, sans-serif; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); letter-spacing: 1px;'>
            Elections 2022 sur la Carte
        </h1>
        <hr style='border: 0; height: 2px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0)); margin: 30px 0;'>

        <div style="display: flex; justify-content: center; margin-bottom: 40px;">
            <div style="position: relative; display: inline-block; line-height: 1;">
                <span style="display: inline-block; color: #3D3D3D; font-size: 32px; font-family: Arial, sans-serif; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); padding: 5px 10px; background-color: #E8E8E8;">Taux de participation</span>
                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border: 2px solid #FF5733; pointer-events: none;"></div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Traitement pour le taux de participation - Tour 1
    dep_participation_tour1 = df_processed.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), votants=('Votants', 'sum')).reset_index()
    dep_participation_tour1['value'] = dep_participation_tour1['votants'] / dep_participation_tour1['inscrits'] * 100
    dep_participation_tour1 = dep_participation_tour1.rename(columns={'Libellé du département': 'departement'}) 
    dep_participation_tour1.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_participation_tour1['code'] = dep_participation_tour1['code'].replace(custom_mapping)
    dep_participation_tour1['code'] = dep_participation_tour1['code'].astype(str)

    # Traitement pour le taux de participation - Tour 2
    dep_participation_tour2 = df_processed2.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), votants=('Votants', 'sum')).reset_index()
    dep_participation_tour2['value'] = dep_participation_tour2['votants'] / dep_participation_tour2['inscrits'] * 100
    dep_participation_tour2 = dep_participation_tour2.rename(columns={'Libellé du département': 'departement'})
    dep_participation_tour2.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_participation_tour2['code'] = dep_participation_tour2['code'].replace(custom_mapping)
    dep_participation_tour2['code'] = dep_participation_tour2['code'].astype(str)

    geojson_path = 'departements-avec-outre-mer.geojson'
    fig_metro1, fig_domtom1, styled_df1 = informations_heatmaps(dep_participation_tour1, geojson_path)  
    fig_metro2, fig_domtom2, styled_df2 = informations_heatmaps(dep_participation_tour2, geojson_path)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_metro1, use_container_width=True)
        st.caption("Tour 1")
    with col2:
        st.plotly_chart(fig_metro2, use_container_width=True)
        st.caption("Tour 2")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_domtom1, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 1") 
    with col2:
        st.plotly_chart(fig_domtom2, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 2")

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 1")
    st.dataframe(styled_df1, use_container_width=True)

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 2") 
    st.dataframe(styled_df2, use_container_width=True)

    #####################################################################################################################

    st.markdown(
        """
        <hr style='border: 0; height: 2px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0)); margin: 30px 0;'>
        
        <div style="display: flex; justify-content: center; margin-bottom: 40px;">
            <div style="position: relative; display: inline-block; line-height: 1;">
                <span style="display: inline-block; color: #3D3D3D; font-size: 32px; font-family: Arial, sans-serif; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); padding: 5px 10px; background-color: #E8E8E8;">Taux d'abstentions</span>
                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border: 2px solid #FF5733; pointer-events: none;"></div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Traitement pour le taux d'abstentions - Tour 1
    dep_abstentions_tour1 = df_processed.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), abstentions=('Abstentions', 'sum')).reset_index()
    dep_abstentions_tour1['value'] = dep_abstentions_tour1['abstentions'] / dep_abstentions_tour1['inscrits'] * 100
    dep_abstentions_tour1 = dep_abstentions_tour1.rename(columns={'Libellé du département': 'departement'})
    dep_abstentions_tour1.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_abstentions_tour1['code'] = dep_abstentions_tour1['code'].replace(custom_mapping)
    dep_abstentions_tour1['code'] = dep_abstentions_tour1['code'].astype(str)

    # Traitement pour le taux d'abstentions - Tour 2
    dep_abstentions_tour2 = df_processed2.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), abstentions=('Abstentions', 'sum')).reset_index()
    dep_abstentions_tour2['value'] = dep_abstentions_tour2['abstentions'] / dep_abstentions_tour2['inscrits'] * 100
    dep_abstentions_tour2 = dep_abstentions_tour2.rename(columns={'Libellé du département': 'departement'})
    dep_abstentions_tour2.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_abstentions_tour2['code'] = dep_abstentions_tour2['code'].replace(custom_mapping)
    dep_abstentions_tour2['code'] = dep_abstentions_tour2['code'].astype(str)

    fig_metro1, fig_domtom1, styled_df1 = informations_heatmaps(dep_abstentions_tour1, geojson_path)
    fig_metro2, fig_domtom2, styled_df2 = informations_heatmaps(dep_abstentions_tour2, geojson_path)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_metro1, use_container_width=True)
        st.caption("Tour 1")
    with col2:
        st.plotly_chart(fig_metro2, use_container_width=True)
        st.caption("Tour 2")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_domtom1, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 1")
    with col2:
        st.plotly_chart(fig_domtom2, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 2")

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 1")
    st.dataframe(styled_df1, use_container_width=True)

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 2")
    st.dataframe(styled_df2, use_container_width=True)

    #####################################################################################################################

    st.markdown(
        """
        <hr style='border: 0; height: 2px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0)); margin: 30px 0;'>
        
        <div style="display: flex; justify-content: center; margin-bottom: 40px;">
            <div style="position: relative; display: inline-block; line-height: 1;">
                <span style="display: inline-block; color: #3D3D3D; font-size: 32px; font-family: Arial, sans-serif; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); padding: 5px 10px; background-color: #E8E8E8;">Taux de votes Exprimés</span>
                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border: 2px solid #FF5733; pointer-events: none;"></div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Traitement pour le taux de votes exprimés - Tour 1
    dep_exprimes_tour1 = df_processed.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), exprimes=('Exprimés', 'sum')).reset_index()
    dep_exprimes_tour1['value'] = dep_exprimes_tour1['exprimes'] / dep_exprimes_tour1['inscrits'] * 100
    dep_exprimes_tour1 = dep_exprimes_tour1.rename(columns={'Libellé du département': 'departement'})
    dep_exprimes_tour1.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_exprimes_tour1['code'] = dep_exprimes_tour1['code'].replace(custom_mapping)
    dep_exprimes_tour1['code'] = dep_exprimes_tour1['code'].astype(str)

    # Traitement pour le taux de votes exprimés - Tour 2
    dep_exprimes_tour2 = df_processed2.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), exprimes=('Exprimés', 'sum')).reset_index()
    dep_exprimes_tour2['value'] = dep_exprimes_tour2['exprimes'] / dep_exprimes_tour2['inscrits'] * 100
    dep_exprimes_tour2 = dep_exprimes_tour2.rename(columns={'Libellé du département': 'departement'})
    dep_exprimes_tour2.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_exprimes_tour2['code'] = dep_exprimes_tour2['code'].replace(custom_mapping)
    dep_exprimes_tour2['code'] = dep_exprimes_tour2['code'].astype(str)

    fig_metro1, fig_domtom1, styled_df1 = informations_heatmaps(dep_exprimes_tour1, geojson_path)
    fig_metro2, fig_domtom2, styled_df2 = informations_heatmaps(dep_exprimes_tour2, geojson_path)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_metro1, use_container_width=True)
        st.caption("Tour 1")
    with col2:
        st.plotly_chart(fig_metro2, use_container_width=True)
        st.caption("Tour 2")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_domtom1, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 1")
    with col2:
        st.plotly_chart(fig_domtom2, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 2")

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 1")
    st.dataframe(styled_df1, use_container_width=True)

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 2")
    st.dataframe(styled_df2, use_container_width=True)

    #####################################################################################################################

    st.markdown(
        """
        <hr style='border: 0; height: 2px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0)); margin: 30px 0;'>
        
        <div style="display: flex; justify-content: center; margin-bottom: 40px;">
            <div style="position: relative; display: inline-block; line-height: 1;">
                <span style="display: inline-block; color: #3D3D3D; font-size: 32px; font-family: Arial, sans-serif; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); padding: 5px 10px; background-color: #E8E8E8;">Taux de votes Exprimés</span>
                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border: 2px solid #FF5733; pointer-events: none;"></div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Traitement pour le taux de votes blancs - Tour 1
    dep_blancs_tour1 = df_processed.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), blancs=('Blancs', 'sum')).reset_index()
    dep_blancs_tour1['value'] = dep_blancs_tour1['blancs'] / dep_blancs_tour1['inscrits'] * 100
    dep_blancs_tour1 = dep_blancs_tour1.rename(columns={'Libellé du département': 'departement'})
    dep_blancs_tour1.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_blancs_tour1['code'] = dep_blancs_tour1['code'].replace(custom_mapping)
    dep_blancs_tour1['code'] = dep_blancs_tour1['code'].astype(str)

    # Traitement pour le taux de votes blancs - Tour 2
    dep_blancs_tour2 = df_processed2.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), blancs=('Blancs', 'sum')).reset_index()
    dep_blancs_tour2['value'] = dep_blancs_tour2['blancs'] / dep_blancs_tour2['inscrits'] * 100
    dep_blancs_tour2 = dep_blancs_tour2.rename(columns={'Libellé du département': 'departement'})
    dep_blancs_tour2.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_blancs_tour2['code'] = dep_blancs_tour2['code'].replace(custom_mapping)
    dep_blancs_tour2['code'] = dep_blancs_tour2['code'].astype(str)

    fig_metro1, fig_domtom1, styled_df1 = informations_heatmaps(dep_blancs_tour1, geojson_path)
    fig_metro2, fig_domtom2, styled_df2 = informations_heatmaps(dep_blancs_tour2, geojson_path)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_metro1, use_container_width=True)
        st.caption("Tour 1")
    with col2:
        st.plotly_chart(fig_metro2, use_container_width=True)
        st.caption("Tour 2")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_domtom1, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 1")
    with col2:
        st.plotly_chart(fig_domtom2, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 2")

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 1")
    st.dataframe(styled_df1, use_container_width=True)

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 2")
    st.dataframe(styled_df2, use_container_width=True)

    #####################################################################################################################

    st.markdown(
        """
        <hr style='border: 0; height: 2px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0)); margin: 30px 0;'>
        
        <div style="display: flex; justify-content: center; margin-bottom: 40px;">
            <div style="position: relative; display: inline-block; line-height: 1;">
                <span style="display: inline-block; color: #3D3D3D; font-size: 32px; font-family: Arial, sans-serif; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); padding: 5px 10px; background-color: #E8E8E8;">Taux de vote Nuls</span>
                <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border: 2px solid #FF5733; pointer-events: none;"></div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Traitement pour le taux de votes nuls - Tour 1
    dep_nuls_tour1 = df_processed.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), nuls=('Nuls', 'sum')).reset_index()
    dep_nuls_tour1['value'] = dep_nuls_tour1['nuls'] / dep_nuls_tour1['inscrits'] * 100
    dep_nuls_tour1 = dep_nuls_tour1.rename(columns={'Libellé du département': 'departement'})
    dep_nuls_tour1.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_nuls_tour1['code'] = dep_nuls_tour1['code'].replace(custom_mapping)
    dep_nuls_tour1['code'] = dep_nuls_tour1['code'].astype(str)

    # Traitement pour le taux de votes nuls - Tour 2
    dep_nuls_tour2 = df_processed2.groupby(['Libellé du département', 'Code du département']).agg(inscrits=('Inscrits', 'sum'), nuls=('Nuls', 'sum')).reset_index()
    dep_nuls_tour2['value'] = dep_nuls_tour2['nuls'] / dep_nuls_tour2['inscrits'] * 100
    dep_nuls_tour2 = dep_nuls_tour2.rename(columns={'Libellé du département': 'departement'})
    dep_nuls_tour2.rename(columns={'Code du département': 'code'}, inplace=True)
    dep_nuls_tour2['code'] = dep_nuls_tour2['code'].replace(custom_mapping)
    dep_nuls_tour2['code'] = dep_nuls_tour2['code'].astype(str)

    fig_metro1, fig_domtom1, styled_df1 = informations_heatmaps(dep_nuls_tour1, geojson_path)
    fig_metro2, fig_domtom2, styled_df2 = informations_heatmaps(dep_nuls_tour2, geojson_path)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_metro1, use_container_width=True)
        st.caption("Tour 1")
    with col2:
        st.plotly_chart(fig_metro2, use_container_width=True)
        st.caption("Tour 2")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_domtom1, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 1")
    with col2:
        st.plotly_chart(fig_domtom2, use_container_width=True)
        st.caption("Territoires d'outre-mer - Tour 2")

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 1")
    st.dataframe(styled_df1, use_container_width=True)

    st.markdown("### Départements avec les taux les plus extrêmes - Tour 2")
    st.dataframe(styled_df2, use_container_width=True)

    ##########################################################################################################################

    st.title("Carte des vainqueurs par département")

    # Pour le premier tour
    fig_tour1 = create_france_winner_map(df_processed, geojson_path)

    # Pour le second tour
    fig_tour2 = create_france_winner_map(df_processed2, geojson_path)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_tour1, use_container_width=True)
        st.caption("Tour 1")
    with col2:
        st.plotly_chart(fig_tour2, use_container_width=True)
        st.caption("Tour 2")

    ##############################################################################################################################    

    # Traitement pour les scores des candidats - Tour 1
    dep_scores_tour1 = df_processed.groupby(['Libellé du département', 'Code du département']).agg(
        votants=('Votants', 'sum'),
        emmanuel_macron=('voix_Emmanuel_MACRON', 'sum'),
        marine_le_pen=('voix_Marine_LE_PEN', 'sum'), 
        jean_luc_melenchon=('voix_Jean-Luc_MÉLENCHON', 'sum'),
        eric_zemmour=('voix_Eric_ZEMMOUR', 'sum')
    ).reset_index()

    for candidate in ['emmanuel_macron', 'marine_le_pen', 'jean_luc_melenchon', 'eric_zemmour']:
        dep_scores_tour1[candidate] = dep_scores_tour1[candidate] / dep_scores_tour1['votants'] * 100

    dep_scores_tour1 = dep_scores_tour1.rename(columns={'Libellé du département': 'departement'}) 
    dep_scores_tour1.rename(columns={'Code du département': 'code'}, inplace=True)

    dep_scores_tour1['code'] = dep_scores_tour1['code'].replace(custom_mapping)
    dep_scores_tour1['code'] = dep_scores_tour1['code'].astype(str)

    # Traitement pour les scores des candidats - Tour 2  
    dep_scores_tour2 = df_processed2.groupby(['Libellé du département', 'Code du département']).agg(
        votants=('Votants', 'sum'),  
        emmanuel_macron=('voix_Emmanuel_MACRON', 'sum'),
        marine_le_pen=('voix_Marine_LE_PEN', 'sum')
    ).reset_index()

    for candidate in ['emmanuel_macron', 'marine_le_pen']:
        dep_scores_tour2[candidate] = dep_scores_tour2[candidate] / dep_scores_tour2['votants'] * 100
        
    dep_scores_tour2 = dep_scores_tour2.rename(columns={'Libellé du département': 'departement'})
    dep_scores_tour2.rename(columns={'Code du département': 'code'}, inplace=True)

    dep_scores_tour2['code'] = dep_scores_tour2['code'].replace(custom_mapping) 
    dep_scores_tour2['code'] = dep_scores_tour2['code'].astype(str)

    candidates = ['Emmanuel Macron', 'Marine Le Pen', 'Jean-Luc Mélenchon', 'Éric Zemmour'] 
    candidate_columns = ['emmanuel_macron', 'marine_le_pen', 'jean_luc_melenchon', 'eric_zemmour']

    for candidate, column in zip(candidates, candidate_columns):
        st.markdown(f"### Scores de {candidate}")
        
        fig_metro1, fig_domtom1, styled_df1 = candidate_score_heatmaps(dep_scores_tour1, geojson_path, column)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_metro1, use_container_width=True) 
            st.caption(f"{candidate} - Tour 1")
        
        with col2:
            if candidate in ['Emmanuel Macron', 'Marine Le Pen']:
                fig_metro2, fig_domtom2, styled_df2 = candidate_score_heatmaps(dep_scores_tour2, geojson_path, column)
                st.plotly_chart(fig_metro2, use_container_width=True)
                st.caption(f"{candidate} - Tour 2")
                
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_domtom1, use_container_width=True)
            st.caption(f"{candidate} - DOM-TOM - Tour 1")
        
        with col2:    
            if candidate in ['Emmanuel Macron', 'Marine Le Pen']:
                st.plotly_chart(fig_domtom2, use_container_width=True)
                st.caption(f"{candidate} - DOM-TOM - Tour 2")

        st.markdown(f"### Départements avec les scores les plus extrêmes pour {candidate} - Tour 1")
        st.dataframe(styled_df1, use_container_width=True)
        
        if candidate in ['Emmanuel Macron', 'Marine Le Pen']:        
            st.markdown(f"### Départements avec les scores les plus extrêmes pour {candidate} - Tour 2")
            st.dataframe(styled_df2, use_container_width=True)