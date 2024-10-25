import streamlit as st 
import pandas as pd
import folium
from streamlit_folium import st_folium

from card import write_card


def portfolio() : 
    

    def underlined_subheader(text):
        st.markdown(f"<h3 style='text-decoration: underline;'>{text}</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image('./images/photo.png', width=150)

    with col2:
        st.image('./images/efrei.png', width=340)

    st.title('Bonjour ! Je suis Sassi De Laat 👋')
    st.write("""
    <p style="font-size:22px; text-align: justify;">Je suis étudiante en Data Science à <u>EFREI Paris Panthéon-Assass</u>,
    passionné par l'intelligence artificielle et le Big Data. Je suis toujours à la recherche de nouveaux
    défis et d'opportunités pout apprendre et évoluer dans mon domaine.</p>  
    """, unsafe_allow_html=True)

    st.divider()

    underlined_subheader('Myself on a map  🌍')

    col1, col2 = st.columns([0.5, 1])

    with col1:
        school = [48.7889, 2.3638]
        home = [48.8376444, 2.3012905]
        work = [48.7878925, 2.4461739]

        center_lat = (school[0] + home[0] + work[0]) / 3
        center_lon = (school[1] + home[1] + work[1]) / 3

        center = [center_lat, center_lon]

        # Create a map centered around Paris
        m = folium.Map(location=center, zoom_start=11, tiles='cartodbpositron')

        def create_emoji_icon(emoji):
            return folium.CustomIcon(
                icon_image=f'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">{emoji}</text></svg>',
                icon_size=(30, 30),
                icon_anchor=(15, 15),
            )
            
        folium.Marker(location=work, icon=create_emoji_icon('🏦')).add_to(m)
        folium.Marker(location=home, icon=create_emoji_icon('🏠')).add_to(m)
        folium.Marker(location=school, icon=create_emoji_icon('🏛️')).add_to(m)

        # Display the map in Streamlit
        st_folium(m, height=300)

    with col2:
        st.write("<u><b>Map Legend</b></u>", unsafe_allow_html=True)
        st.write("🏦 - Travail: Université Créteil")
        st.write("🏠 - Maison")
        st.write("🏛️ - Ecole: EFREI Paris")
        
        st.write("<u><b>About My Locations</b></u>", unsafe_allow_html=True)
        st.write("""
            <p style="font-size:22px; text-align: justify;">Cette carte présente les lieux clés de ma vie quotidienne. 
            De mes études à l'EFREI Paris à mon stage dans le laboratoire de l'Université de Créteil, 
            et ma maison entre les deux, elle représente mon voyage au cœur de Paris en tant que 
            Data Engineer et Data Analyst en herbe.</p>
        """, unsafe_allow_html=True)
        
    st.divider()

    underlined_subheader('Projets Personnels 📁')

    col1, col2, col3 = st.columns(3)

    with col1:
        write_card(
            "🗂️ Algorithme de classification de brevets", 
            ['TensorFlow', 'PyTorch', 'Numpy', 'Scikit-learn'], 
            "", 
            "Juin 2024"
        )

    with col2:
        write_card(
            "🏘️ Algorithme prédictif de la valeur immobilière de biens",
            ['Pandas', 'Numpy', 'Matplotlib', ' Scikit-learn'],
            "Sassidl/Property-value-prediction",
            "Mai 2024"
        )

    with col3:
        write_card(
            "📊  Analyse des élections présidentielles françaises 2022",
            ['Java', '', '', ''],
            "",
        "Novembre 2023"
        )
    
        
    st.divider()

    underlined_subheader('Mes formations 🎓')
    st.write("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.75, 1])

    with col1:
        st.write('<br>', unsafe_allow_html=True)
        st.write('<br>', unsafe_allow_html=True)
        st.image('./images/efrei.png', width=250)

    with col2:
        st.write("<h4><u><b>EFREI Paris</b></u></h4>", unsafe_allow_html=True)
        st.write("<p style=font-size:21px>🖥️ M1: Data Science & Data Engineering</p>", unsafe_allow_html=True)
        st.write("<p style=font-size:21px>🌎 L3: Semestre à l'Internatial - Concordia, Montréal</p>", unsafe_allow_html=True)
        st.write("<p style=font-size:21px>📚 L1 & L2: Licence Biologie Numérique - Classe préparatoire</p>", unsafe_allow_html=True)
        
    st.write('<br>', unsafe_allow_html=True)
    st.write('<br>', unsafe_allow_html=True)

    col1, col2 = st.columns([0.75, 1])
