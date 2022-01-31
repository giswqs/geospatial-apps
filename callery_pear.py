import streamlit as st
from streamlit_option_menu import option_menu
from apps import callery_home, callery_photos  # import your app modules here

st.set_page_config(page_title="Callery Pear", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = {
    "callery_home": {"title": "Home", "icon": "house"},
    "callery_photos": {"title": "Photos", "icon": "images"},
    # "upload": {"title": "Upload", "icon": "cloud-upload"},
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

        Web App URL: <https://icons.getbootstrap.com>
    """
    )

for app in apps:
    if apps[app]["title"] == selected:
        eval(f"{app}.app()")
        break
