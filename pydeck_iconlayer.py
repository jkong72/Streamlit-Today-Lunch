import pydeck as pdk
import pandas as pd

icon_data = {
    "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
    "width": 128,
    "height":128,
    "anchorY": 128
}
data = pd.read_json("https://raw.githubusercontent.com/uber-common/deck.gl-data/master/website/bart-stations.json")
data['icon_data']= None

for i in data.index:
     data['icon_data'][i] = icon_data

view_state = pdk.ViewState(
    longitude=-122.22,
    latitude=37.76,
    zoom=9,
    pitch=50
)

icon_layer = pdk.Layer(
    type='IconLayer',
    data=data,
    get_icon='icon_data',
    get_size=4,
    pickable=True,
    size_scale=15,
    get_position='coordinates'
)
tooltip = {
   "html": "<b>Address:</b> {address} <br/> <b>Station:</b> {name}",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}
r = pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip=tooltip)
r.show()