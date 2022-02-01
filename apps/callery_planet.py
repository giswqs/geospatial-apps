import os
import ee
import geemap.foliumap as geemap
import streamlit as st
import pandas as pd


def app():

    st.title("Planet Imagery")
    st.markdown("""
    See https://www.planet.com for more information.
    """)

    df = st.session_state["locations"]

    col1, col2, col3, _, col4, col5, col6, col7, _ = st.columns(
        [3, 0.7, 1, 0.2, 1, 1, 1, 1, 1])

    Map = geemap.Map(locate_control=True, plugin_LatLngPopup=False)

    Map.add_basemap("HYBRID")
    Map.add_basemap("ROADMAP")

    names = df["Name"].values.tolist()
    names.sort()

    with col1:
        name = st.selectbox("Select a location", names)
    latitude = df[df["Name"] == name]["latitude"].values[0]
    longitude = df[df["Name"] == name]["longitude"].values[0]

    with col2:
        ratio = st.radio("Planet imagery", ('Quarterly', "Monthly"))

    with col3:
        year = st.slider("Select a year", 2016, 2021, 2020)

    with col5:
        lat = st.text_input("Center latitude", latitude)

    with col6:
        lon = st.text_input("Center longitude", longitude)

    with col7:
        zoom = st.slider("Zoom", 1, 22, 17)

    if ratio == "Quarterly":
        with col4:
            quarter = st.slider("Select a quarter", 1, 4, 1)
            Map.add_planet_by_quarter(year, quarter)
    else:
        with col4:
            month = st.slider("Select a month", 1, 12, 1)
            Map.add_planet_by_month(year, month)

    states = ee.FeatureCollection("TIGER/2018/States")
    style = {"color": "000000", "width": 2, "fillColor": "00000000"}
    Map.addLayer(states.style(**style), {}, "US States")
    Map.add_points_from_xy(
        "data/PyCTN.csv", popup=["Name", "latitude", "longitude"], layer_name="Callery Pear Locations")
    Map.set_center(float(lon), float(lat), int(zoom))
    Map.to_streamlit(height=700)
