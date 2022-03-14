import folium
import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap


def app():

    st.title('National Library of Scotland XYZ Layers')
    df = pd.read_csv('data/scotland_xyz.tsv', sep='\t')
    names = df['Name'].values.tolist()
    links = df['URL'].values.tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        left_name = st.selectbox('Select the left layer', names)

    with col2: 
        right_name = st.selectbox('Select the right layer', names, index=1)


    m = leafmap.Map(center=[55.68,-2.98], zoom=6)

    left_layer = folium.TileLayer(
        tiles=links[names.index(left_name)],
        name=left_name,
        attr='National Library of Scotland',
        overlay=True
        
    )
    right_layer = folium.TileLayer(
        tiles=links[names.index(right_name)],
        name=right_name,
        attr='National Library of Scotland',
        overlay=True

    )

    m.split_map(left_layer, right_layer)
    m.to_streamlit(height=800)
