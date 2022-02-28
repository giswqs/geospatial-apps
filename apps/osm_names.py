import requests
import leafmap.foliumap as leafmap
import streamlit as st


def search(name, limit):
    url = 'https://photon.komoot.io/api/'
    r = requests.get(url, params={'q': name, 'limit': limit}).json()
    df = leafmap.geojson_to_df(r, drop_geometry=False)
    df['longitude'] = df['geometry.coordinates'].str[0]
    df['latitude'] = df['geometry.coordinates'].str[1]
    df['country'] = df['countrycode']
    df.drop(['type', 'geometry.coordinates',
            'countrycode'], axis=1, inplace=True)
    return df


def app():

    st.title('Search Geographic Names')
    col1, col2 = st.columns([3, 1])

    m = leafmap.Map(latlon_control=False, center=(40, -100), zoom=4)
    m.add_basemap('HYBRID')
    m.add_basemap('ROADMAP')
    m.add_basemap('OpenStreetMap')

    with col2:
        limit = st.slider("The number of results to return", 1, 5000, 1000)
        name = st.text_input("Enter a name")
        if name:
            try:
                df = search(name, limit)
                if not df.empty:
                    column = st.selectbox(
                        "Filter by", df.columns, index=list(df.columns).index('country')
                    )
                    if "US" in df[column].unique():
                        default = "US"
                    else:
                        default = df[column].unique()
                    filters = st.multiselect(
                        "Select values",
                        df[column].unique(),
                        default=default,
                    )

                    if filters:
                        df = df[df[column].isin(filters)]
                    st.text(f"Found {len(df)} results")
                    leafmap.st_download_button(
                        "Download data", df, csv_sep="\t")
                    m.add_points_from_xy(
                        df,
                        x='longitude',
                        y='latitude',
                        popup=[
                            'name',
                            'longitude',
                            'latitude',
                            'osm_key',
                            'city',
                            'county',
                            'state',
                            'country',
                        ],
                    )
                else:
                    st.error("No results found")
            except Exception as e:
                st.error("No results found")

    with col1:
        m.to_streamlit(height=700)
