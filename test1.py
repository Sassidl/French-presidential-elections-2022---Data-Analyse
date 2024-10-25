import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
st.balloons()
st.write(st.__version__)
 
# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)
 
# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
 
st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})
 
with st.expander("See explanation"):
     st.write("""
         The chart above shows some numbers I picked for you.
         I rolled actual dice for these, so they're *guaranteed* to
         be random.
     """)
     st.image("https://static.streamlit.io/examples/dice.jpg")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")
 
with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")
 
with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")
 
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])
 
with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
 
with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
 
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
 
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
 
 
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
 
st.pydeck_chart(pdk.Deck(
     map_style=None,
     initial_view_state=pdk.ViewState(
         latitude=37.76,
         longitude=-122.4,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
))
from PIL import Image
image = Image.open('sunrise.jpg')
st.image(image, caption='Sunrise by the mountains')
st.markdown('Streamlit is **_really_ cool**.')