"""
IconLayer
=========

Location of biergartens in Germany listed on OpenStreetMap as of early 2020.
"""

import streamlit as st
import pydeck as pdk
import pandas as pd


# Data from OpenStreetMap, accessed via osmpy
DATA_URL = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/biergartens.json"
ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c4/Projet_bi%C3%A8re_logo_v2.png"

icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}

data = pd.read_json(DATA_URL)
data["icon_data"] = None
for i in data.index:
    data["icon_data"][i] = icon_data

st.pydeck_chart(pdk.Deck(
    map_style = 'mapbox://styles/mapbox/light-v9',
    initial_view_state =pdk.ViewState(
         latitude=37.5428959487629,
         longitude=126.677211723637,
         zoom=15,
         pitch=40,
         ),
    layers = [
        pdk.Layer(
            "IconLayer",
            data=data,
            get_icon="icon_data",
            get_size=4,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True,
            )
    ],
    )
)

print (data)

    

r = pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip={"text": "{tags}"})
r.to_html("icon_layer.html")