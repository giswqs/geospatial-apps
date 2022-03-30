import streamlit as st
from streamlit_option_menu import option_menu

# import your app modules here
from apps import split, scotland

st.set_page_config(page_title="Split-panel Map", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = [
    {"func":split.app, "title": "Home", "icon": "house"},
    {"func":scotland.app, "title": "Scotland", "icon": "globe"},
]

titles = [app["title"] for app in apps]
icons = [app["icon"] for app in apps]

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
        Web App URL: <https://gishub.org/split-map>

        Contact Qiusheng Wu (qwu18@utk.edu) if you have any questions or comments.
    """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break