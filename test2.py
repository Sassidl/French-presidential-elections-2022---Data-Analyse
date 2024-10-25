import streamlit as st
import pandas as pd
import numpy as np
 
st.title('Plotting data in streamlit the native way !')
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])
 
st.write('Below is a randomn dataFrame:', chart_data)
 
#https://docs.streamlit.io/library/api-reference/charts/st.line_chart
st.write('Plotting the column "a" with st.line_chart')
st.line_chart(chart_data['a'])
st.write('Plotting all the columns with st.line_chart')
st.line_chart(chart_data)
 
#https://docs.streamlit.io/library/api-reference/charts/st.area_chart
st.write('Plotting the same dataframe in an area chart with st.area_chart')
st.area_chart(chart_data)
 
#https://docs.streamlit.io/library/api-reference/charts/st.bar_chart
st.write('Plotting the same dataframe in a bar chart with st.')
st.bar_chart(chart_data)
 
#https://docs.streamlit.io/library/api-reference/charts/st.map
df_map = pd.DataFrame(
     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
     columns=['lat', 'lon'])
st.write('Display a map with points on it. Using an other randomn dataframe')
st.map(df_map)