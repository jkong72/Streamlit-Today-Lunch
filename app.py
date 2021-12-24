from pydeck.bindings.view_state import ViewState
import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk

from secure import mapbox

# csv 가공
df = pd.read_csv('data/restaurant.csv')

df.dropna(inplace=True)

df['대분류'] = df['분류'].str.split(' > ').str[1]
df['세부분류'] = df['분류'].str.split(' > ').str[2]
df.loc[df['대분류'].isna(),'대분류']= '기타'
df.loc[(df['대분류']=='한식')&(df['세부분류'].isna()),'세부분류'] = '기타한식'
df.loc[df['대분류']=='한식','대분류'] = '한식-'+df.loc[df['대분류']=='한식', '세부분류']


df.drop(columns='분류', inplace=True)
df.columns = ['이름', 'lon', 'lat', '대분류', '세부분류']
# print (df.columns)
# print (df)
MAPBOX_API_KEY = mapbox()
# MAP API

center = [['연희직업전문학교', 126.677211723637, 37.5428959487629]]
center_df = pd.DataFrame(center)
center_df.columns = ['이름', 'lon', 'lat']
# print (center_df.loc[0,'lon'])
# print (df)

CENTER_ICON_URL = 'https://cdn-icons-png.flaticon.com/512/167/167707.png' # Sample. MUST be change later.
center_icon_data = {
    "url": CENTER_ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}

ICON_URL = 'https://cdn-icons-png.flaticon.com/512/857/857718.png'
icon_data = {
    "url": ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}

# DF에 아이콘 데이터 삽입
df['icon_data'] = None
# length = df.shape[0]
for i in df.index:
    df['icon_data'][i] = icon_data
center_df['icon_data'] = None
center_df['icon_data'][0] = center_icon_data

# print (df['대분류'].unique())
kind = df['대분류'].unique()
# kind = [x for x in kind if np.isnan(kind) ==False]
kind = sorted(kind)


# print (df.loc[df['대분류'] == kind[0],][['이름', 'lon', 'lat']])

st.title('타이틀')

# ALL_ICON_LAYERS = {
#     kind[0]: pdk.Layer(
#             'IconLayer',
#             data=df[['이름', 'lat', 'lon', 'icon_data',kind[0]]],
#             get_icon='icon_data',
#             get_size=3,
#             size_scale=20,
#             get_position=['lon', 'lat'],
#             pickable=True,
#         )
# }

st. sidebar.markdown('### 거리별 필터')
df['x거리'] = abs (center[0][1]*100000 - df['lon']*100000)
df['y거리'] = abs (center[0][2]*100000 - df['lat']*100000)
df['distance'] = (df['x거리']**2 + df['y거리']**2)**0.5

# 위와 같지만 변수 사용을 최소화한 코드. (no hard coding)
# df['distance'] = (((center[0][1]*100000 - df['lon']*100000)**2)+((center[0][2]*100000 - df['lat']*100000)**2)**0.5)

distance = st.sidebar.slider('반경 (m)', min_value=0, max_value=700, value=150, step=10)
df = df.loc[df['distance'] <= distance,]

STORE_LAYERS = {}
for i in range(0,len(kind)):
    STORE_LAYERS[kind[i]] = pdk.Layer(
        'IconLayer',
        data=df.loc[df['대분류'] == kind[i],][['이름', 'lon', 'lat', 'icon_data']],
        get_icon='icon_data',
        get_size=4,
        size_scale=10,
        get_position=['lon', 'lat'],
        pickable=True
    )

st. sidebar.markdown('### 메뉴별 필터')

# selected_layers = [
#     layer for layer_name, layer in STORE_LAYERS.items()
#     if st.sidebar.checkbox(layer_name, False)]

layers = st.sidebar.multiselect('', STORE_LAYERS.keys(), default = ['패스트푸드', '한식-국밥', '한식-한정식'])
selected_layers = [
    layer for layer_name, layer in STORE_LAYERS.items()
    if layer_name in layers]
    

    
print (selected_layers)



st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=center_df.loc[0,'lat'], 
        longitude=center_df.loc[0,'lon'], 
        pitch=40, 
        zoom=15,
        ),
    layers=[
    pdk.Layer(
    'IconLayer',
    data=center_df,
    get_icon='icon_data',
    get_size=8,
    size_scale=10,
    get_position=['lon', 'lat'],
    pickable=True,
    ),
    selected_layers],
    tooltip={'text':'{이름}'},
    ))

# st. pydeck_chart(pdk.Deck(
#     map_style='mapbox://styles/mapbox/light-v9',
#     initial_view_state=pdk.ViewState(
#         latitude=center_df.loc[0,'lat'], 
#         longitude=center_df.loc[0,'lon'], 
#         pitch=40, 
#         zoom=15,
#         ),
#     layers=[
#         pdk.Layer(
#             'IconLayer',
#             data=center_df,
#             get_icon='icon_data',
#             get_size=8,
#             size_scale=15,
#             get_position=['lon', 'lat'],
#             pickable=True,
#         ),
        # pdk.Layer(
        #     'IconLayer',
        #     data=df[['이름', 'lat', 'lon', 'icon_data']],
        #     get_icon='icon_data',
        #     get_size=3,
        #     size_scale=20,
        #     get_position=['lon', 'lat'],
        #     pickable=True,
        # )
#     ],
#     tooltip={'text':'{이름}'}
#     )
# )

st.title('여긴 끝')