import streamlit as st
from streamlit_option_menu import option_menu
# import your app modules here
from apps import callery_home, callery_naip, callery_photos, callery_planet

st.set_page_config(page_title="Callery Pear", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = {
    "callery_home": {"title": "Home", "icon": "house"},
    "callery_photos": {"title": "Photos", "icon": "images"},
    "callery_naip": {"title": "NAIP Imagery (1-m)", "icon": "globe"},
    "callery_planet": {"title": "Planet Imagery (5-m)", "icon": "camera"},
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
        Web App URL: <https://spatial.utk.edu/callery-pear>

        Contact Qiusheng Wu (qwu18@utk.edu) if you have any questions or comments.
    """
    )

for app in apps:
    if apps[app]["title"] == selected:
        eval(f"{app}.app()")
        break
