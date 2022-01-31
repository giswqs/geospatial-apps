import pandas as pd
import streamlit as st
import geemap.foliumap as geemap


def app():
    st.title("Home")

    st.markdown(
        """
    ##### Map of Callery Pear locations in the State of Tennessee

    """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        df = pd.read_csv("data/PyCTN.csv")
        st.session_state["locations"] = df
        names = df["Name"].values.tolist()
        names.sort()
        name = st.selectbox("Select a location", names)

    with col2:
        zoom = st.slider("Zoom", 1, 22, 8)

    with col3:
        st.info(
            """
        Click the layer control in the upper-righh corner of the map to toggle between basemaps.

        """
        )

    latitude = df[df["Name"] == name]["latitude"].values[0]
    longitude = df[df["Name"] == name]["longitude"].values[0]

    m = geemap.Map(center=(latitude, longitude),
                   zoom=zoom, locate_control=True)
    m.add_basemap("ROADMAP")
    m.add_basemap("HYBRID")
    m.add_points_from_xy(
        "data/PyCTN.csv", popup=["Name", "latitude", "longitude"], layer_name="Callery Pear Locations")
    m.to_streamlit(height=700)
