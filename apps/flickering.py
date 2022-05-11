import ee
import geemap.foliumap as geemap
import streamlit as st
from streamlit_folium import st_folium

m = geemap.Map()
dem = ee.Image("USGS/SRTMGL1_003")
m.addLayer(dem, {}, "DEM")
st_data = st_folium(m, width=1000)