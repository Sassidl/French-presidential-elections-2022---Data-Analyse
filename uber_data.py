import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import binned_statistic
from scipy.interpolate import make_interp_spline

@st.cache_data
def load_uber_data():
    path2 = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
    
    df = pd.read_csv(path2, delimiter=',')
    
    df['tpep_pickup_datetime'] = df['tpep_pickup_datetime'].map(pd.to_datetime)
    df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].map(pd.to_datetime)
    
    def get_dom(dt):
        return dt.day #is an attribute of the datetime object
    
    df['day']= df ['tpep_pickup_datetime'].map(get_dom)
    
    def get_weekday(dt):
        return dt.weekday() 
    
    df['weekday']= df['tpep_pickup_datetime'].map(get_weekday)
    return df


def uber_data_analysis():
    st.title('Uber Pickups in NYC')
    
    # Load the data
    df = load_uber_data()
    
    # Display basic information
    st.subheader('Dataset Information')
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")
    
    # Display the first few rows
    st.subheader('First Few Rows of the Dataset')
    st.write(df.head())
    
    # Display summary statistics
    st.subheader('Summary Statistics')
    st.write(df.describe())

    # Data cleaning and preprocessing
    st.subheader('Data Cleaning and Preprocessing')

    
    def count_rows(rows):
        return len(rows)

    fig, (ax, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 14), gridspec_kw={'height_ratios': [3, 3]})

    # Premier graphique (courbe lissée) - Inchangé
    bins = np.linspace(df['trip_distance'].min(), df['trip_distance'].quantile(0.99), 100)
    bin_means, bin_edges, _ = binned_statistic(df['trip_distance'], df['total_amount'], statistic='mean', bins=bins)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    spl = make_interp_spline(bin_centers, bin_means, k=3)
    smooth_distance = np.linspace(bin_centers.min(), bin_centers.max(), 300)
    smooth_amount = spl(smooth_distance)

    ax.plot(smooth_distance, smooth_amount, color='blue', linewidth=2)

    ax.set_title('Relation lissée entre Distance et Montant total des trajets Uber (Avril 2014)', fontsize=16)
    ax.set_xlabel('Distance (miles)', fontsize=12)
    ax.set_ylabel('Montant total moyen ($)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)

    ax.set_xlim(0, df['trip_distance'].quantile(0.99))
    y_max = smooth_amount.max() * 1.1
    ax.set_ylim(0, y_max)

    # Deuxième graphique (boxplot) - Modifié pour limiter à 50 miles
    df_filtered = df[df['trip_distance'] <= 50]
    df_filtered['distance_bin'] = pd.cut(df_filtered['trip_distance'], 
                                        bins=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
                                        labels=['0-5', '5-10', '10-15', '15-20', '20-25', 
                                                '25-30', '30-35', '35-40', '40-45', '45-50'])

    sns.boxplot(x='distance_bin', y='total_amount', data=df_filtered, ax=ax2)

    ax2.set_title('Distribution des montants par tranches de distance (jusqu\'à 50 miles)', fontsize=14)
    ax2.set_xlabel('Tranches de distance (miles)', fontsize=12)
    ax2.set_ylabel('Montant total ($)', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)

    # Ajuster les limites de l'axe y pour le boxplot
    y_max_boxplot = df_filtered['total_amount'].quantile(0.99)
    ax2.set_ylim(0, 210)

    # Ajuster l'espacement entre les sous-graphiques
    plt.tight_layout()

    # Affichage du graphique dans Streamlit
    st.pyplot(fig)
    
    df['duration'] = df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']
    df['duration_in_minutes'] = df['duration'].dt.total_seconds() / 60
    
    fig, ax = plt.subplots(figsize=(10, 6))

    # Création de l'histogramme
    ax.hist(df['duration'].dt.total_seconds() / 60, bins=30, range=(0, 60), 
            color='blue', edgecolor='black')

    # Personnalisation du graphique
    ax.set_title('Répartition de la durée des trajets', fontsize=16)
    ax.set_xlabel('Durée (minutes)', fontsize=12)
    ax.set_ylabel('Nombre de trajets', fontsize=12)
    ax.set_xlim(0, 60)
    ax.grid(True)

    # Ajustement de la mise en page
    plt.tight_layout()

    # Affichage du graphique dans Streamlit
    st.pyplot(fig)

    df['hour'] = df['tpep_pickup_datetime'].dt.hour
    hourly_prices = df.groupby('hour')['fare_amount'].mean().reset_index()
        
    fig, ax = plt.subplots(figsize=(10, 6))

    # Création des bins pour l'histogramme
    bins = [x - 0.5 for x in range(25)]  # Crée des bins de -0.5 à 24.5

    # Création de l'histogramme
    ax.hist(df['hour'], bins=bins, alpha=0.7, align='mid', rwidth=0.8, color='skyblue', edgecolor='black')

    # Personnalisation du graphique
    ax.set_xlabel('Heure de la journée', fontsize=12)
    ax.set_ylabel('Nombre de trajets', fontsize=12)
    ax.set_title('Répartition des trajets Uber par heure de départ', fontsize=15)
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels(range(0, 24))
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='both', labelsize=12)

    # Ajustement de la mise en page
    plt.tight_layout()

    # Affichage du graphique dans Streamlit
    st.pyplot(fig)
    
    hourly_stats = df['hour'].value_counts().sort_index()

    # Affichage des heures de pointe
    peak_hours = hourly_stats.nlargest(3)
    st.write("Heures de pointe (top 3) :")
    for hour, count in peak_hours.items():
        st.write(f"{hour}h : {count} trajets")

    # Affichage des heures creuses
    off_peak_hours = hourly_stats.nsmallest(3)
    st.write("Heures creuses (bottom 3) :")
    for hour, count in off_peak_hours.items():
        st.write(f"{hour}h : {count} trajets")
    
    df['rounded_distance'] = df['trip_distance'].round()

    df['tips_boolean'] = df['tip_amount'] > 0

    tips_percentage = df.groupby('rounded_distance').agg({
        'tips_boolean': ['count','sum']
    }).reset_index()

    tips_percentage.columns = ['distance','number_customers','total_number_tips']

    tips_percentage['tips_percentage'] = (tips_percentage['total_number_tips'] / tips_percentage['number_customers']) * 100

    tips_percentage.head()
    
    fig, ax = plt.subplots(figsize=(12, 6))

    # Création du nuage de points
    ax.scatter(tips_percentage['distance'], tips_percentage['tips_percentage'], alpha=0.5)

    # Ajout de la ligne de tendance
    z = np.polyfit(tips_percentage['distance'], tips_percentage['tips_percentage'], 1)
    p = np.poly1d(z)
    ax.plot(tips_percentage['distance'], p(tips_percentage['distance']), "r--", alpha=0.8)

    # Personnalisation du graphique
    ax.set_title('Pourcentage de trajets avec pourboire en fonction de la distance', fontsize=16)
    ax.set_xlabel('Distance (en miles)', fontsize=12)
    ax.set_ylabel('Pourcentage de trajets avec pourboire', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlim(0, 25)

    # Ajustement de la mise en page
    plt.tight_layout()

    # Affichage du graphique dans Streamlit
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(12, 6))

    # Création du graphique à barres
    sns.barplot(x='hour', y='fare_amount', data=hourly_prices, ax=ax)

    # Personnalisation du graphique
    ax.set_title('Prix moyen des trajets par heure', fontsize=16)
    ax.set_xlabel('Heure de la journée', fontsize=12)
    ax.set_ylabel('Prix moyen ($)', fontsize=12)
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels(range(0, 24))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajustement de la mise en page
    plt.tight_layout()

    # Affichage du graphique dans Streamlit
    st.pyplot(fig)


    # Identification des heures les plus chères et les moins chères
    most_expensive_hour = hourly_prices.loc[hourly_prices['fare_amount'].idxmax()]
    least_expensive_hour = hourly_prices.loc[hourly_prices['fare_amount'].idxmin()]

    st.write(f"Heure la plus chère : {most_expensive_hour['hour']}h avec un prix moyen de ${most_expensive_hour['fare_amount']:.2f}")
    st.write(f"Heure la moins chère : {least_expensive_hour['hour']}h avec un prix moyen de ${least_expensive_hour['fare_amount']:.2f}")

    # Calcul de la différence de prix entre les heures de pointe et les heures creuses
    peak_hours = hourly_prices['fare_amount'].nlargest(3).mean()
    off_peak_hours = hourly_prices['fare_amount'].nsmallest(3).mean()
    price_difference = peak_hours - off_peak_hours

    st.write(f"Différence moyenne de prix entre les heures de pointe et les heures creuses : ${price_difference:.2f}")
        
        
    ##########FOLIUM###############   
        
    import folium
    import webbrowser
    import os
    from folium.plugins import HeatMap
    from streamlit_folium import folium_static

    def create_heatmap(data, lat_col, lon_col, title):
        center_lat = data[lat_col].mean()
        center_lon = data[lon_col].mean()
        m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

        heat_data = [[row[lat_col], row[lon_col]] for index, row in data.iterrows()]
        HeatMap(heat_data).add_to(m)

        return m

    # Chargement des données (assurez-vous que votre DataFrame 'df' est correctement chargé)
    # df = pd.read_csv('votre_fichier.csv')

    # Titre de l'application
    st.title('Cartes de chaleur des trajets Uber à New York')

    # Création des cartes de chaleur
    pickup_map = create_heatmap(df, 'pickup_latitude', 'pickup_longitude', 'Emplacements de prise en charge')
    dropoff_map = create_heatmap(df, 'dropoff_latitude', 'dropoff_longitude', 'Emplacements de dépôt')

    # Affichage des cartes
    st.header('Carte de chaleur des emplacements de prise en charge')
    folium_static(pickup_map)

    st.header('Carte de chaleur des emplacements de dépôt')
    folium_static(dropoff_map)

    # Statistiques supplémentaires
    st.header('Statistiques sur les emplacements')

    # Top 5 des zones de prise en charge
    st.subheader('Top 5 des zones de prise en charge')
    top_pickup = df.groupby(['pickup_latitude', 'pickup_longitude']).size().sort_values(ascending=False).head()
    st.write(top_pickup)

    # Top 5 des zones de dépôt
    st.subheader('Top 5 des zones de dépôt')
    top_dropoff = df.groupby(['dropoff_latitude', 'dropoff_longitude']).size().sort_values(ascending=False).head()
    st.write(top_dropoff)

    # Distance moyenne des trajets
    st.subheader('Distance moyenne des trajets')
    avg_distance = df['trip_distance'].mean()
    st.write(f"La distance moyenne des trajets est de {avg_distance:.2f} miles")