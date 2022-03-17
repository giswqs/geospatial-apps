import ee
import folium
import streamlit as st
import geemap.foliumap as geemap
import geemap.colormaps as cm


@st.cache
def uploaded_file_to_gdf(data):
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.getbuffer())

    if file_path.lower().endswith(".kml"):
        gpd.io.file.fiona.drvsupport.supported_drivers["KML"] = "rw"
        gdf = gpd.read_file(file_path, driver="KML")
    else:
        gdf = gpd.read_file(file_path)

    return gdf


def app():

    st.title('Nighttime Light Data Analysis')

    # markdown = """The split-panel map requires two layers: `left_layer` and `right_layer`. The layer instance can be a string representing a basemap, or an HTTP URL to a Cloud Optimized GeoTIFF (COG), or a folium TileLayer instance."""
    # st.markdown(markdown)

    with st.expander("Click to see the data sources", False):
        markdown = """
        
            - [VIIRS Stray Light Corrected Nighttime Day/Night Band Composites Version 1](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMSLCFG) (463.83 m)
        
        """
        st.markdown(markdown)

    row1_col1, _, row1_col2 = st.columns([3, 0.03, 1])

    Map = geemap.Map(
        add_google_map=False,
        plugin_LatLngPopup=False,
        locate_control=True,
        plugin_Draw=True,
    )
    Map.add_basemap("HYBRID")
    Map.add_basemap("TERRAIN")

    fc = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
    names = fc.aggregate_array('country_na').getInfo()
    names = list(set(names))
    names.sort()
    palettes = cm.list_colormaps()

    nightlight = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG")

    with row1_col2:
        with st.form("get_NTL"):
            years = st.slider("Select years", 2014, 2021, [2014, 2021])
            months = st.slider("Select months", 1, 12, [1, 12])
            min_max = st.slider(
                "Select visualization min-max", 0.0, 50.0, [0.0, 10.0], 0.5
            )
            palette = st.selectbox(
                "Select a palette", palettes, index=palettes.index("gist_earth")
            )
            countries = st.multiselect("Select countries", names)
            diff_chk = st.checkbox("NTL differencing: end_year - start_year")
            trans_chk = st.checkbox("Make low values transparent")
            split = st.checkbox("Split-panel map")

            submitted = st.form_submit_button("Submit")

            if submitted:

                start_a = ee.Date.fromYMD(years[0], months[0], 1)
                end_a = start_a.advance(months[1] - months[0], "month")

                start_b = ee.Date.fromYMD(years[1], months[0], 1)
                end_b = start_b.advance(months[1] - months[0], "month")

                ntl_a = nightlight.filterDate(start_a, end_a).mean().select("avg_rad")
                ntl_b = nightlight.filterDate(start_b, end_b).mean().select("avg_rad")

                if countries:
                    selected_countries = ee.FeatureCollection(
                        'USDOS/LSIB_SIMPLE/2017'
                    ).filter(ee.Filter.inList("country_na", countries))
                    country_style = selected_countries.style(
                        **{'color': '000000', 'width': 2, 'fillColor': '00000000'}
                    )
                    Map.addLayer(country_style, {}, "Countries")
                    Map.centerObject(selected_countries, 4)

                    ntl_a = ntl_a.clip(selected_countries)
                    ntl_b = ntl_b.clip(selected_countries)

                if trans_chk:
                    ntl_a = ntl_a.updateMask(ntl_a.gt(min_max[0]))
                    ntl_b = ntl_b.updateMask(ntl_b.gt(min_max[0]))

                if split:
                    left_layer = geemap.ee_tile_layer(
                        ntl_a,
                        {
                            'min': min_max[0],
                            'max': min_max[1],
                            'palette': cm.get_palette(palette, 15),
                        },
                        f'NTL {years[0]}',
                    )
                    right_layer = geemap.ee_tile_layer(
                        ntl_b,
                        {
                            'min': min_max[0],
                            'max': min_max[1],
                            'palette': cm.get_palette(palette, 15),
                        },
                        f'NTL {years[1]}',
                    )
                    Map.split_map(left_layer, right_layer)
                else:
                    Map.addLayer(
                        ntl_a,
                        {
                            'min': min_max[0],
                            'max': min_max[1],
                            'palette': cm.get_palette(palette, 15),
                        },
                        f'NTL {years[0]}',
                    )
                    Map.addLayer(
                        ntl_b,
                        {
                            'min': min_max[0],
                            'max': min_max[1],
                            'palette': cm.get_palette(palette, 15),
                        },
                        f'NTL {years[1]}',
                    )

                    if diff_chk:
                        diff = ntl_b.subtract(ntl_a)
                        Map.addLayer(
                            diff,
                            {
                                'min': min_max[0],
                                'max': min_max[1],
                                'palette': cm.get_palette(palette, 15),
                            },
                            f'NTL {years[1]} - {years[0]}',
                        )

    with row1_col1:
        Map.to_streamlit(height=650)
