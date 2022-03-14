import ee
import folium
import streamlit as st
import geemap.foliumap as geemap


def app():

    st.title('Split-panel Map')

    markdown = """The split-panel map requires two layers: `left_layer` and `right_layer`. The layer instance can be a string representing a basemap, or an HTTP URL to a Cloud Optimized GeoTIFF (COG), or a folium TileLayer instance."""
    st.markdown(markdown)

    st.header('Using basemaps')
    with st.echo():
        m = geemap.Map(height=500)
        m.split_map(left_layer='TERRAIN', right_layer='OpenTopoMap')
        m.to_streamlit(height=600)

    st.header('Using COG')
    with st.echo():
        m = geemap.Map(height=600, center=[39.4948, -108.5492], zoom=12)
        url = 'https://opendata.digitalglobe.com/events/california-fire-2020/pre-event/2018-02-16/pine-gulch-fire20/1030010076004E00.tif'
        url2 = 'https://opendata.digitalglobe.com/events/california-fire-2020/post-event/2020-08-14/pine-gulch-fire20/10300100AAC8DD00.tif'
        m.split_map(url, url2)
        m.to_streamlit(height=600)

    st.header('Using folium TileLayer')
    with st.echo():
        m = geemap.Map(center=[40, -100], zoom=4)

        url1 = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2001_Land_Cover_L48/wms?'
        url2 = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2019_Land_Cover_L48/wms?'

        left_layer = folium.WmsTileLayer(
            url=url1,
            layers='NLCD_2001_Land_Cover_L48',
            name='NLCD 2001',
            attr='MRLC',
            fmt="image/png",
            transparent=True,
        )
        right_layer = folium.WmsTileLayer(
            url=url2,
            layers='NLCD_2019_Land_Cover_L48',
            name='NLCD 2019',
            attr='MRLC',
            fmt="image/png",
            transparent=True,
        )

        m.split_map(left_layer, right_layer)
        m.add_legend(builtin_legend='NLCD')
        m.to_streamlit(height=600)


    st.header('Using Earth Engine layers')
    with st.echo():
        m = geemap.Map(center=[39.3322, -106.7349], zoom=10)
        srtm = ee.Image("USGS/SRTMGL1_003")
        hillshade = ee.Terrain.hillshade(srtm)
        vis = {
            'min': 0,
            'max': 5000,
            'palette': ["006633", "E5FFCC", "662A00", "D8D8D8", "F5F5F5"],
        }
        left_layer = geemap.ee_tile_layer(hillshade, name='Hillshade')
        right_layer = geemap.ee_tile_layer(srtm, vis, name='DEM')
        m.split_map(left_layer, right_layer)
        m.to_streamlit(height=600)
