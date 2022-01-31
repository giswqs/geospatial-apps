import streamlit as st
import geemap.foliumap as geemap


def app():
    st.title("Photos")

    st.markdown(
        """
    ##### Photos of Callery Pear locations along James White Parkway, Knoxville, TN (see [Google Map](https://goo.gl/maps/ogfSyf4k11pLLJVP9))

    """
    )

    expander = st.expander("Click to show the photos", True)

    links = [
        "https://i.imgur.com/lAXIidc.jpg",
        "https://i.imgur.com/R8X17Cr.jpg",
        "https://i.imgur.com/mHsz3NY.jpg"
    ]

    with expander:
        st.image(links)

    center = (35.964760, -83.899257)
    m = geemap.Map(center=center, zoom=18, locate_control=True)
    m.add_basemap("ROADMAP")
    m.add_basemap("HYBRID")
    m.add_marker(location=center, tooltip="Callery Pear")
    m.to_streamlit(height=700)
