import streamlit as st
import geemap.foliumap as geemap


def app():
    st.title("Home")

    st.markdown(
        """
    ##### Map of Callery Pear locations in the State of Tennessee

    """
    )

    st.info(
        """
    Click the layer control in the upper-righh corner of the map to toggle between basemaps.

    """
    )

    m = geemap.Map(center=(35.857892, -84.517822), zoom=8, locate_control=True)
    m.add_basemap("ROADMAP")
    m.add_basemap("HYBRID")
    m.add_points_from_xy("data/PyCTN.csv", popup=["Name", "latitude", "longitude"], layer_name="Callery Pear Locations")
    m.to_streamlit(height=700)
