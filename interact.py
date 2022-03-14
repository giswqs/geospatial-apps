import streamlit as st
from streamlit_option_menu import option_menu

# import your app modules here
from apps import get_bounds

st.set_page_config(page_title="Streamlit Folium", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = {
    "get_bounds": {"title": "Home", "icon": "house"},
}

titles = [app["title"] for app in apps.values()]
icons = [app["icon"] for app in apps.values()]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        Web App URL: <https://gishub.org/streamlit-folium>

        Contact Qiusheng Wu (qwu18@utk.edu) if you have any questions or comments.
    """
    )

for app in apps:
    if apps[app]["title"] == selected:
        eval(f"{app}.app()")
        break
