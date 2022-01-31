import os
import ee
import geemap.foliumap as geemap
import streamlit as st


def app():

    st.title("NAIP Imagery")

    st.markdown("""
    NAIP: National Agriculture Imagery Program. See this [link](https://developers.google.com/earth-engine/datasets/catalog/USDA_NAIP_DOQQ) for more information.

    """)

    df = st.session_state["locations"]
    names = df["Name"].values.tolist()
    names.sort()

    col1, col2, col3, col5, col6, col7, _ = st.columns(
        [1.8, 2, 2, 1, 1, 1, 1])

    Map = geemap.Map(plugin_Draw=True, Draw_export=True)
    # with col1:
    #     basemap = st.selectbox(
    #         "Select a basemap", geemap.folium_basemaps.keys(), index=1)
    Map.add_basemap("HYBRID")
    Map.add_basemap("ROADMAP")

    with col1:
        name = st.selectbox("Select a location", names)
    latitude = df[df["Name"] == name]["latitude"].values[0]
    longitude = df[df["Name"] == name]["longitude"].values[0]

    # roi = ee.FeatureCollection("users/giswqs/MRB/NWI_HU8_Boundary_Simplify")
    # roi = ee.FeatureCollection(
    #     "TIGER/2018/States").filter(ee.Filter.eq("NAME", "Tennessee"))
    roi = ee.Geometry.Point([longitude, latitude]).buffer(1000)

    style = {"color": "000000", "width": 2, "fillColor": "00000000"}

    with col2:
        checkbox = st.checkbox("Add NAIP imagery", value=True)

    with col5:
        lat = st.text_input("Center latitude", latitude)

    with col6:
        lon = st.text_input("Center longitude", longitude)

    with col7:
        zoom = st.slider("Zoom", 1, 22, 17)

    if checkbox:
        with col3:
            year = st.slider("Select a year", 2003, 2021, 2018)
        naip = ee.ImageCollection("USDA/NAIP/DOQQ")
        naip = naip.filter(ee.Filter.calendarRange(year, year, "year"))
        naip = naip.filterBounds(roi)

        # 2005, 2006, 2007,
        vis_params = {"bands": ["N", "R", "G"]}
        if year in [2005, 2006, 2007]:
            vis_params = {"bands": ["R", "G", "B"]}

        Map.addLayer(naip, vis_params, f"NAIP {year}")

    # Map.addLayer(roi.style(**style), {}, "Tennessee")

    Map.add_points_from_xy(
        "data/PyCTN.csv", popup=["Name", "latitude", "longitude"], layer_name="Callery Pear Locations")

    Map.set_center(float(lon), float(lat), int(zoom))
    Map.to_streamlit(width=1400, height=700)
