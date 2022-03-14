import folium
import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap


def app():

    st.title('National Library of Scotland XYZ Layers')
    df = pd.read_csv('data/scotland_xyz.tsv', sep='\t')
    basemaps = leafmap.folium_basemaps
    names = df['Name'].values.tolist() + list(basemaps.keys())
    links = df['URL'].values.tolist() + list(basemaps.values())

    col1, col2, col3, col4, col5, col6 = st.columns([3, 3, 1, 1, 1, 1.5])
    with col1:
        left_name = st.selectbox(
            'Select the left layer', names, index=names.index('HYBRID')
        )

    with col2:
        right_name = st.selectbox(
            'Select the right layer',
            names,
            index=names.index('Great Britain - Bartholomew Half Inch, 1897-1907'),
        )

    with col3:
        # lat = st.slider('Latitude', -90.0, 90.0, 55.68, step=0.01)
        lat = st.text_input('Latitude', " 55.68")

    with col4:
        # lon = st.slider('Longitude', -180.0, 180.0, -2.98, step=0.01)
        lon = st.text_input('Longitude', "-2.98")

    with col5:
        # zoom = st.slider('Zoom', 1, 24, 6, step=1)
        zoom = st.text_input('Zoom', "6")

    with col6:
        checkbox = st.checkbox('Add OS 25 inch')

    m = leafmap.Map(center=[float(lat), float(lon)], zoom=int(zoom), locate_control=True, draw_control=False)

    if left_name in basemaps:
        left_layer = basemaps[left_name]
    else:
        left_layer = folium.TileLayer(
            tiles=links[names.index(left_name)],
            name=left_name,
            attr='National Library of Scotland',
            overlay=True,
        )

    if right_name in basemaps:
        right_layer = basemaps[right_name]
    else:
        right_layer = folium.TileLayer(
            tiles=links[names.index(right_name)],
            name=right_name,
            attr='National Library of Scotland',
            overlay=True,
        )

    if checkbox:
        for index, name in enumerate(names):
            if 'OS 25 inch' in name:
                m.add_tile_layer(
                    links[index], name, attribution='National Library of Scotland'
                )

    m.split_map(left_layer, right_layer)
    m.to_streamlit(height=600)
