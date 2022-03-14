from unicodedata import bidirectional
from urllib import response
import folium
import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium


def app():

    st.title('Streamlit folium bidirectional functionality')

    col1, col2 = st.columns([3, 1])
    m = leafmap.Map()

    with col1:
        output = m.to_streamlit(bidirectional=True)

    with col2:
        try:
            center = m.st_map_center(output)
            st.text_input('Map Center Latitude', center[0])
            st.text_input('Map center Longitude', center[1])
            st.write(output)
        except:
            pass
