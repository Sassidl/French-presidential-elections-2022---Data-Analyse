import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import colorsys
import seaborn as sns

@st.cache_data
def load_data():
    file_path = 'resultats-par-niveau-burvot-t1-france-entiere.xlsx'
    df = pd.read_excel(file_path, sheet_name='Résultats par niveau BurVot T1 France Entière')
    return df

@st.cache_data
def load_data2():
    file_path = 'resultats-par-niveau-burvot-t2-france-entiere.xlsx'
    df = pd.read_excel(file_path)
    return df

##########################################################################################################################################


def informations_heatmaps(df, geojson_path, color='RdYlBu_r'):
    # Load the GeoJSON file
    gdf = gpd.read_file(geojson_path)
    
    # Separate metropolitan France and overseas territories
    gdf_metro = gdf[gdf['code'].str.len() == 2]
    df_metro = df[df['code'].astype(str).str.len() == 2]
    df_overseas = df[df['code'].astype(str).str.len() > 2]
    
    # Merge the GeoDataFrame with the data for metropolitan France
    merged_metro = gdf_metro.merge(df_metro, left_on='code', right_on='code', how='left')
    
    # Create choropleth map for metropolitan France
    fig_metro = px.choropleth_mapbox(merged_metro, 
                                     geojson=merged_metro.geometry, 
                                     locations=merged_metro.index, 
                                     color='value',
                                     color_continuous_scale=color,
                                     range_color=(df['value'].min(), df['value'].max()),
                                     hover_name='departement',
                                     hover_data={'value': ':.2f'},
                                     mapbox_style="carto-positron",
                                     zoom=4.5, center={"lat": 46.8566, "lon": 2.3522},
                                     opacity=0.7,
                                     labels={'value': 'Taux'})
    
    fig_metro.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=600,
        title={
            'text': "France Métropolitaine",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
    # Create a figure for overseas territories
    fig_domtom = go.Figure()
    
    num_regions = len(df_overseas)
    cols = int(np.ceil(np.sqrt(num_regions)))
    rows = int(np.ceil(num_regions / cols))
    
    color_scale = px.colors.sequential.Viridis
    norm = plt.Normalize(vmin=df['value'].min(), vmax=df['value'].max())
    
    for i, (_, region) in enumerate(df_overseas.iterrows()):
        row = i // cols
        col = i % cols
        color_idx = int(norm(region['value']) * (len(color_scale) - 1))
        fig_domtom.add_trace(go.Scatter(
            x=[col, col+1, col+1, col, col],
            y=[-row, -row, -(row+1), -(row+1), -row],
            fill="toself",
            fillcolor=color_scale[color_idx],
            line_color="black",
            text=f"{region['departement']}<br>{region['value']:.2f}%",
            hoverinfo="text",
            mode="lines"
        ))
        fig_domtom.add_annotation(
            x=col+0.5, y=-(row+0.5),
            text=f"<b>{region['departement']}</b><br>{region['value']:.2f}%",
            showarrow=False,
            font=dict(size=10, color='black'),
            align='center',
            bgcolor='white',
            bordercolor='black',
            borderwidth=1,
            borderpad=4,
            opacity=0.9
        )
    
    fig_domtom.update_layout(
        title={
            'text': "Territoires d'Outre-Mer",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=400, width=800,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Create DataFrame with extreme participation rates
    df_sorted = df.sort_values('value', ascending=False)
    highest_3 = df_sorted.head(3)
    lowest_3 = df_sorted.tail(3)
    result_df = pd.concat([highest_3, lowest_3])
    result_df = result_df.rename(columns={
        'departement': 'Département',
        'value': 'Taux (%)'
    })
    result_df['Taux (%)'] = result_df['Taux (%)'].apply(lambda x: f"{x:.2f}")
    
    # Style the DataFrame
    styled_df = result_df.style.set_properties(**{
        'background-color': 'lightyellow',
        'color': 'black',
        'border-color': 'white'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', 'lightblue'), ('color', 'black'), ('font-weight', 'bold')]
    }, {
        'selector': '.index_name, .index_header',
        'props': 'display:none;'
    }])
    
    styled_df = styled_df.highlight_max(subset=['Taux (%)'], color='lightgreen')
    styled_df = styled_df.highlight_min(subset=['Taux (%)'], color='lightcoral')
    
    # Hide index
    styled_df = styled_df.hide(axis='index')
    
    return fig_metro, fig_domtom, styled_df



##########################################################################################################################################


def create_france_winner_map(df, geojson_path):
    # Calculer le gagnant pour chaque département
    winner_by_dept = df.groupby('Code du département').apply(lambda x: pd.Series({
        'gagnant': x[[col for col in x.columns if col.startswith('voix/ins_')]].idxmax(axis=1).iloc[0].replace('voix/ins_', ''),
        'pourcentage': x[[col for col in x.columns if col.startswith('voix/ins_')]].max(axis=1).iloc[0]
    }))
    
    # Charger le GeoJSON
    gdf = gpd.read_file(geojson_path)
    
    # Fusionner avec les données des gagnants
    gdf = gdf.merge(winner_by_dept, left_on='code', right_index=True, how='left')
    
    # Définir une palette de couleurs pour les candidats
    color_map = {
        'Emmanuel_MACRON': '#0000FF',  # Bleu
        'Marine_LE_PEN': '#C41E3A',    # Rouge foncé
        'Jean-Luc_MÉLENCHON': '#FF0000',  # Rouge vif
        'Éric_ZEMMOUR': '#8B4513',  # Marron
        'Valérie_PÉCRESSE': '#0066CC',  # Bleu clair
        'Yannick_JADOT': '#00FF00',  # Vert
        'Jean_LASSALLE': '#FFA500',  # Orange
        'Fabien_ROUSSEL': '#800080',  # Violet
        'Nicolas_DUPONT-AIGNAN': '#808080',  # Gris
        'Anne_HIDALGO': '#FFC0CB',  # Rose
        'Philippe_POUTOU': '#8B0000',  # Rouge foncé
        'Nathalie_ARTHAUD': '#FF69B4'  # Rose vif
    }
    
    # Créer la carte
    fig = px.choropleth_mapbox(gdf,
                               geojson=gdf.geometry,
                               locations=gdf.index,
                               color='gagnant',
                               color_discrete_map=color_map,
                               hover_name='nom',
                               hover_data=['gagnant', 'pourcentage'],
                               mapbox_style="carto-positron",
                               center={"lat": 46.2276, "lon": 2.2137},
                               zoom=4.5,
                               opacity=0.7)
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600)
    
    
    return fig

##########################################################################################################################################


def candidate_score_heatmaps(df, geojson_path, candidate, color='RdYlBu_r'):
    # Load the GeoJSON file
    gdf = gpd.read_file(geojson_path)
    
    # Separate metropolitan France and overseas territories
    gdf_metro = gdf[gdf['code'].str.len() == 2]  
    df_metro = df[df['code'].astype(str).str.len() == 2]
    df_overseas = df[df['code'].astype(str).str.len() > 2]
    
    # Merge the GeoDataFrame with the data for metropolitan France
    merged_metro = gdf_metro.merge(df_metro, left_on='code', right_on='code', how='left')
    
    # Create choropleth map for metropolitan France
    fig_metro = px.choropleth_mapbox(merged_metro, 
                                     geojson=merged_metro.geometry, 
                                     locations=merged_metro.index, 
                                     color=candidate,
                                     color_continuous_scale=color,
                                     range_color=(df[candidate].min(), df[candidate].max()),
                                     hover_name='departement',
                                     hover_data={candidate: ':.2f%'},
                                     mapbox_style="carto-positron",
                                     zoom=4.5, center={"lat": 46.8566, "lon": 2.3522},
                                     opacity=0.7,
                                     labels={candidate: 'Score'})
    
    fig_metro.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=600,
        title={
            'text': f"France Métropolitaine - {candidate}",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
    # Create a figure for overseas territories 
    fig_domtom = go.Figure()

    num_regions = len(df_overseas)
    cols = int(np.ceil(np.sqrt(num_regions)))
    rows = int(np.ceil(num_regions / cols))
    
    color_scale = px.colors.sequential.Viridis
    norm = plt.Normalize(vmin=df[candidate].min(), vmax=df[candidate].max())
    
    for i, (_, region) in enumerate(df_overseas.iterrows()):
        row = i // cols 
        col = i % cols
        color_idx = int(norm(region[candidate]) * (len(color_scale) - 1))
        fig_domtom.add_trace(go.Scatter(
            x=[col, col+1, col+1, col, col],
            y=[-row, -row, -(row+1), -(row+1), -row],
            fill="toself",
            fillcolor=color_scale[color_idx],
            line_color="black",
            text=f"{region['departement']}<br>{region[candidate]:.2f}%",
            hoverinfo="text",
            mode="lines"       
        ))
        fig_domtom.add_annotation(
            x=col+0.5, y=-(row+0.5),
            text=f"<b>{region['departement']}</b><br>{region[candidate]:.2f}%", 
            showarrow=False,
            font=dict(size=10, color='black'),
            align='center',
            bgcolor='white',
            bordercolor='black',
            borderwidth=1,
            borderpad=4,
            opacity=0.9
        )

    fig_domtom.update_layout(
        title={
            'text': f"Territoires d'Outre-Mer - {candidate}",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=400, width=800,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    # Create DataFrame with extreme scores  
    df_sorted = df.sort_values(candidate, ascending=False)
    highest_3 = df_sorted.head(3)
    lowest_3 = df_sorted.tail(3)
    result_df = pd.concat([highest_3, lowest_3])
    result_df = result_df.rename(columns={
        'departement': 'Département', 
        candidate: 'Score (%)'
    })
    result_df['Score (%)'] = result_df['Score (%)'].apply(lambda x: f"{x:.2f}")

    # Style the DataFrame
    styled_df = result_df.style.set_properties(**{
        'background-color': 'lightyellow',
        'color': 'black',
        'border-color': 'white'   
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', 'lightblue'), ('color', 'black'), ('font-weight', 'bold')]
    }, {
        'selector': '.index_name, .index_header',
        'props': 'display:none;'  
    }])

    styled_df = styled_df.highlight_max(subset=['Score (%)'], color='lightgreen')
    styled_df = styled_df.highlight_min(subset=['Score (%)'], color='lightcoral')

    # Hide index
    styled_df = styled_df.hide(axis='index')

    return fig_metro, fig_domtom, styled_df



###########################################################################################################################################

def rename_columns(df):
    new_names = {}
    columns_to_drop = []
    
    for i, candidate in enumerate(candidates):
        base_index = 21 + i * 7
        
        if base_index + 6 < len(df.columns):
            new_names.update({
                df.columns[base_index + 2]: f'candidat_{candidate}',
                df.columns[base_index + 4]: f'voix_{candidate}',
                df.columns[base_index + 5]: f'voix/ins_{candidate}',
                df.columns[base_index + 6]: f'voix/exp_{candidate}'
            })
        
    for i, candidate in enumerate(candidates):
        base_index = 21 + i * 7
        
        if base_index + 6 < len(df.columns):
            columns_to_drop.extend([df.columns[base_index], df.columns[base_index + 1], df.columns[base_index + 3]])
        
    # Rename columns
    df = df.rename(columns=new_names)
    
    # Drop unnecessary columns
    df = df.drop(columns=columns_to_drop)
    
    return df

def rename_columns2(df):
    new_names = {}
    columns_to_drop = []
    
    for i, candidate in enumerate(candidates2):
        base_index = 21 + i * 7
        
        if base_index + 6 < len(df.columns):
            new_names.update({
                df.columns[base_index + 2]: f'candidat_{candidate}',
                df.columns[base_index + 4]: f'voix_{candidate}',
                df.columns[base_index + 5]: f'voix/ins_{candidate}',
                df.columns[base_index + 6]: f'voix/exp_{candidate}'
            })
        
    for i, candidate in enumerate(candidates2):
        base_index = 21 + i * 7
        
        if base_index + 6 < len(df.columns):
            columns_to_drop.extend([df.columns[base_index], df.columns[base_index + 1], df.columns[base_index + 3]])
        
    # Rename columns
    df = df.rename(columns=new_names)
    
    # Drop unnecessary columns
    df = df.drop(columns=columns_to_drop)
    
    return df


##########################################################################################################################################


def create_columns_html(columns, columns_per_row):
    html = '<div style="overflow-x: auto;"><table style="width: 100%; border-collapse: collapse;">'
    for i in range(0, len(columns), columns_per_row):
        html += '<tr>'
        for col in columns[i:i+columns_per_row]:
            html += f'<td style="border: 1px solid black; padding: 5px; white-space: nowrap;">{col}</td>'
        html += '</tr>'
    html += '</table></div>'
    return html


# Mapping dictionary to align DataFrame department names to GeoJSON names
name_mapping = {
    "Alpes-de-Haute-Provence": "Alpes-de-Haute-Provence",
    "Alpes-Maritimes": "Alpes-Maritimes",
    "Ain": "Ain",
    "Aisne": "Aisne",
    "Allier": "Allier",
    "Bouches-du-Rhône": "Bouches-du-Rhône",
    "Côte-d'Or": "Côte-d'Or",
    "Côtes-d'Armor": "Côtes-d'Armor",
    "Deux-Sèvres": "Deux-Sèvres",
    "Hauts-de-Seine": "Hauts-de-Seine",
    "Territoire de Belfort": "Territoire de Belfort",
    "Seine-Saint-Denis": "Seine-Saint-Denis",
    "La Réunion": "Réunion",
    "Français établis hors de France": "Français établis à l'étranger",
    "Saint-Martin/Saint-Barthélemy": "Saint-Martin",
}

candidates = [
    "Nathalie_ARTHAUD", "Fabien_ROUSSEL", "Emmanuel_MACRON", "Jean_LASSALLE",
    "Marine_LE_PEN", "Eric_ZEMMOUR", "Jean-Luc_MÉLENCHON", "Anne_HIDALGO",
    "Yannick_JADOT", "Valérie_PÉCRESSE", "Philippe_POUTOU", "Nicolas_DUPONT-AIGNAN"
]

candidates2 = [
    "Emmanuel_MACRON","Marine_LE_PEN"
]

custom_mapping = {
    '2A': '201',  # Corse-du-Sud
    '2B': '202',  # Haute-Corse
    'ZZ': '980', 'ZA': '981', 'ZB': '982', 'ZC': '983', 'ZD': '984',
    'ZM': '985', 'ZN': '986', 'ZP': '987', 'ZX': '988', 'ZS': '989', 'ZW': '990'
}


####################################################################################################################################

def calculate_percentages(df, vote_type):
    total_votes = df['Exprimés'].sum() if vote_type == 'exp' else df['Inscrits'].sum()
    candidate_columns = [col for col in df.columns if col.startswith('voix_')]
    
    results = pd.DataFrame({
        'Candidat': [col.replace('voix_', '') for col in candidate_columns],
        'Voix': df[candidate_columns].sum(),
    })
    
    results['Pourcentage'] = (results['Voix'] / total_votes) * 100
    return results.sort_values('Pourcentage', ascending=False)

def create_podium(df, title, subtitle, vote_type):
    results = calculate_percentages(df, vote_type)
    top_candidates = results.head(3)  # Prend jusqu'à 3 candidats
    
    st.markdown(f"<h2 style='text-align: center; color: #1E1E1E;'>{title}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #3D3D3D; margin-bottom: 20px;'>{subtitle}</h3>", unsafe_allow_html=True)
    
    num_candidates = len(top_candidates)
    if num_candidates == 2:
        col1, col2 = st.columns(2)
        columns = [col1, col2]
        colors = ['#FFD700', '#C0C0C0']  # Or, Argent
        order = [0, 1]
    else:
        col1, col2, col3 = st.columns(3)
        columns = [col1, col2, col3]
        colors = ['#C0C0C0', '#FFD700', '#CD7F32']  # Argent, Or, Bronze
        order = [1, 0, 2]  # Ordre pour placer le gagnant au milieu
    
    max_percentage = top_candidates['Pourcentage'].max()
    base_height = 50
    
    for i, idx in enumerate(order[:num_candidates]):
        candidate = top_candidates.iloc[idx]
        height = base_height + int((candidate['Pourcentage'] / max_percentage) * 300)
        
        with columns[i]:
            st.markdown(f"""
            <div style="height:{400-height}px;"></div>
            <div style="background-color: {colors[i]}; width: 100%; height: {height}px; display: flex; flex-direction: column; justify-content: flex-end; align-items: center;">
                <span style="background-color: rgba(255,255,255,0.7); padding: 5px; font-weight: bold;">
                    {candidate['Pourcentage']:.2f}%
                </span>
            </div>
            <div style="text-align: center; margin-top: 10px;">
                <div style="font-weight: bold;">{candidate['Candidat']}</div>
                <div>Voix: {candidate['Voix']:,}</div>
            </div>
            """, unsafe_allow_html=True)
            
            
def calculate_global_stats(df):
    total_inscrits = df['Inscrits'].sum()
    total_abstentions = df['Abstentions'].sum()
    total_votants = df['Votants'].sum()
    total_blancs = df['Blancs'].sum()
    total_nuls = df['Nuls'].sum()
    total_exprimes = df['Exprimés'].sum()

    return {
        "Taux de participation": (total_votants / total_inscrits) * 100,
        "Taux d'abstention": (total_abstentions / total_inscrits) * 100,
        "Taux de votes blancs": (total_blancs / total_inscrits) * 100,
        "Taux de votes nuls": (total_nuls / total_inscrits) * 100,
        "Taux de votes exprimés": (total_exprimes / total_inscrits) * 100
    }

def display_comparative_stats(df1, df2):
    stats1 = calculate_global_stats(df1)
    stats2 = calculate_global_stats(df2)
    
    st.markdown("<h2 style='text-align: center; color: #1E1E1E;'>Comparaison des Statistiques Globales</h2>", unsafe_allow_html=True)
    
    for stat in stats1.keys():
        st.markdown(f"<h3 style='color: #2c3e50; margin-top: 30px;'>{stat}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="
                background-color: #f0f2f6;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            ">
                <h4 style="margin-bottom: 10px;">1er Tour</h4>
                <p style="
                    font-size: 32px;
                    font-weight: bold;
                    color: #3498db;
                    margin: 0;
                ">{stats1[stat]:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background-color: #f0f2f6;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            ">
                <h4 style="margin-bottom: 10px;">2ème Tour</h4>
                <p style="
                    font-size: 32px;
                    font-weight: bold;
                    color: #e74c3c;
                    margin: 0;
                ">{stats2[stat]:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <br>
            <br>
            <br>
            """, unsafe_allow_html=True)
            
def generate_distinct_colors(n):
    HSV_tuples = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))
    return [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in RGB_tuples]

def create_pie_chart(df, tour):
    total_inscrits = df['Inscrits'].sum()
    
    results = {
        'Abstentions': df['Abstentions'].sum() / total_inscrits * 100,
        'Blancs': df['Blancs'].sum() / total_inscrits * 100,
        'Nuls': df['Nuls'].sum() / total_inscrits * 100
    }
    
    candidat_columns = [col for col in df.columns if col.startswith('voix_')]
    for col in candidat_columns:
        candidat = col.replace('voix_', '')
        results[candidat] = df[col].sum() / total_inscrits * 100
    
    results_sorted = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    
    # Utiliser une palette de couleurs pastel
    colors = sns.color_palette("pastel", len(results_sorted))
    
    fig, ax = plt.subplots(figsize=(14, 10))
    wedges, texts, autotexts = ax.pie(results_sorted.values(), 
                                      labels=results_sorted.keys(), 
                                      autopct=lambda pct: f'{pct:.1f}%' if pct > 2 else '',
                                      pctdistance=0.85,
                                      colors=colors,
                                      wedgeprops=dict(width=0.5, edgecolor='white'))
    
    ax.set_title(f"Résultats du {tour} (en % des inscrits)", fontsize=16, pad=20)
    
    # Légende
    ax.legend(wedges, results_sorted.keys(),
              title="Catégories",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=10)
    
    plt.setp(autotexts, size=9, weight="bold", color="black")
    plt.setp(texts, size=11)
    
    return fig

# Fonction pour calculer le taux de participation de 2022
def calculate_participation_2022(df):
    total_inscrits = df['Inscrits'].sum()
    total_votants = df['Votants'].sum()
    return (total_votants / total_inscrits) * 100

historical_data = {
    '2002': [72.15, 79.59],
    '2007': [83.77, 84.99],
    '2012': [80.35, 81.01],
    '2017': [77.77, 71.96]
}


def aggregate_data1(df):
    # Agréger les données au niveau départemental
    df_agg = df.groupby('Code du département').agg({
        'Inscrits': 'sum',
        'Votants': 'sum',
        'Exprimés': 'sum'
    })
    
    # Calculer le taux de participation
    df_agg['Taux_Participation'] = df_agg['Votants'] / df_agg['Inscrits'] * 100
    
    # Trouver le candidat gagnant et son score pour chaque département
    candidat_columns = [col for col in df.columns if col.startswith('voix_')]
    for col in candidat_columns:
        df_agg[col] = df.groupby('Code du département')[col].sum()
    
    df_agg['Gagnant'] = df_agg[candidat_columns].idxmax(axis=1).str.replace('voix_', '')
    df_agg['Score_Gagnant'] = df_agg[candidat_columns].max(axis=1) / df_agg['Exprimés'] * 100
    
    return df_agg

def create_scatter_plot(df, tour):
    df_agg = aggregate_data1(df)
    
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df_agg, x='Taux_Participation', y='Score_Gagnant', hue='Gagnant', 
                    palette='deep', size='Inscrits', sizes=(20, 500), alpha=0.7)
    
    plt.title(f"Relation entre Taux de Participation et Score du Gagnant par Département ({tour})", fontsize=16)
    plt.xlabel("Taux de Participation (%)", fontsize=12)
    plt.ylabel("Score du Candidat Gagnant (%)", fontsize=12)
    
    sns.regplot(data=df_agg, x='Taux_Participation', y='Score_Gagnant', 
                scatter=False, color='red', line_kws={'linestyle':'--'})
    
    plt.legend(title='Candidat Gagnant', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    return plt.gcf()

def aggregate_data2(df):
    df_agg = df.groupby('Code du département').agg({
        'Inscrits': 'sum',
        'Votants': 'sum',
        'Exprimés': 'sum'
    })
    
    df_agg['Taux_Participation'] = df_agg['Votants'] / df_agg['Inscrits'] * 100
    
    for candidate in ['Emmanuel_MACRON', 'Marine_LE_PEN', 'Jean-Luc_MÉLENCHON']:
        col = f'voix_{candidate}'
        if col in df.columns:
            df_agg[f'score_{candidate}'] = df.groupby('Code du département')[col].sum() / df_agg['Exprimés'] * 100
    
    return df_agg

def create_histograms(df, tour):
    df_agg = aggregate_data2(df)
    
    # Histogramme du taux de participation
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data=df_agg, x='Taux_Participation', kde=True, ax=ax)
    ax.set_title(f"Distribution du Taux de Participation par Département ({tour})", fontsize=14, pad=20)
    ax.set_xlabel("Taux de Participation (%)", fontsize=12)
    ax.set_ylabel("Nombre de Départements", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Histogrammes des scores des candidats sélectionnés
    candidates = ['Emmanuel_MACRON', 'Marine_LE_PEN', 'Jean-Luc_MÉLENCHON']
    fig, axes = plt.subplots(3, 1, figsize=(12, 15))
    fig.suptitle(f"Distribution des Scores des Principaux Candidats par Département ({tour})", 
                 fontsize=16, y=0.98)
    
    for i, candidate in enumerate(candidates):
        col = f'score_{candidate}'
        if col in df_agg.columns:
            sns.histplot(data=df_agg, x=col, kde=True, ax=axes[i])
            axes[i].set_title(candidate.replace('_', ' '), fontsize=12, pad=20)
            axes[i].set_xlabel("Score (%)", fontsize=10)
            axes[i].set_ylabel("Nombre de Départements", fontsize=10)
        else:
            axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.95, hspace=0.4)
    st.pyplot(fig)

