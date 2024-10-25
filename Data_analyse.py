import streamlit as st
from streamlit_option_menu import option_menu


from functions import load_data, load_data2, rename_columns, rename_columns2
from introduction import introduction
from maps import maps
from uber_data import uber_data_analysis
from resultats_cles import resultats_cles
from portfolio import portfolio

# Load the dataset
df_tour1 = load_data()
df_tour1_processed = rename_columns(df_tour1)

# Load the dataset
df_tour2 = load_data2()
df_tour2_processed = rename_columns2(df_tour2)


st.markdown("""
<style>
.reportview-container .main .block-container {
    max-width: 1700px;
    padding-top: 2rem;
    padding-right: 1rem;
    padding-left: 1rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)


# Sidebar menu
with st.sidebar:
    main_menu = option_menu(
        "Navigation",
        ["Portfolio", "Uber Data", "Elections Présidentielles"],
        icons=["house", "car-front", "box-seam-fill"],
        menu_icon="cast",
        default_index=0,
    )

    # Sous-menu pour Elections Présidentielles
    if main_menu == "Elections Présidentielles":
        sub_menu = option_menu(
            "",
            ["Dataset", "Résultats Clés", "Cartes"],
            icons=["bar-chart-line", "key", "globe-europe-africa"],
            menu_icon="cast",
            default_index=0,
        )

# Affichage du contenu basé sur la sélection
if main_menu == "Portfolio":
    portfolio()
elif main_menu == "Uber Data":
    uber_data_analysis()
elif main_menu == "Elections Présidentielles":
    if sub_menu == "Dataset":
        introduction(df_tour1, df_tour1_processed, df_tour2, df_tour2_processed)
    elif sub_menu == "Résultats Clés":
        resultats_cles(df_tour1_processed, df_tour2_processed)
    elif sub_menu == "Cartes":
        maps(df_tour1_processed, df_tour2_processed)