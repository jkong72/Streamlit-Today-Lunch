# IMPORT LIBRARY / PACKAGE
from re import L
from pydeck.bindings.view_state import ViewState
import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
############################################################
# csv 가공
df = pd.read_csv('data/restaurant.csv')

df.dropna(inplace=True)
df.drop_duplicates(['이름'], inplace=True)

df['대분류'] = df['분류'].str.split(' > ').str[1]
df['세부분류'] = df['분류'].str.split(' > ').str[2]
df.loc[df['대분류'].isna(),'대분류']= '기타'
df.loc[(df['대분류']=='한식')&(df['세부분류'].isna()),'세부분류'] = '기타한식'
df.loc[df['대분류']=='한식','대분류'] = '한식-'+df.loc[df['대분류']=='한식', '세부분류']

df.loc[df['이름']=='마수리마라탕', '대분류']= '식사-중식'
df.loc[df['이름']=='사노라면', '대분류']= '식사-분식'
df.loc[df['이름']=='양푼이우거지동태탕', '대분류']= '식사-해물'
df.loc[df['이름']=='향나무 영양탕', '대분류']= '식사-국밥/탕'
df.loc[df['이름']=='가시골염소마을', '대분류']= '육류/고기'
df.loc[df['이름']=='등촌샤브칼국수 서구점', '대분류']= '식사-면류'
df.loc[df['이름']=='채선당PLUS 서구청점', '대분류']= '육류/고기'

df.loc[(df['대분류']=='한식-감자탕')|(df['대분류']=='한식-곰탕')|(df['대분류']=='한식-순대')|(df['대분류']=='한식-찌개,전골')|(df['대분류']=='한식-해장국')|(df['대분류']=='한식-설렁탕')|(df['대분류']=='한식-국밥'),'대분류'] = '식사-국밥/탕'
df.loc[(df['대분류']=='도시락')|(df['대분류']=='한식-한정식')|(df['대분류']=='한식-쌈밥')|(df['대분류']=='한식-죽')|(df['대분류']=='한식-기타한식') ,'대분류']= '식사-한식/도시락'
df.loc[(df['대분류']=='간식')|(df['대분류']=='샐러드'),'대분류'] = '디저트/간식/샐러드'
df.loc[(df['대분류']=='한식-국수')|(df['대분류']=='한식-냉면'),'대분류'] = '식사-면류'
df.loc[(df['대분류']=='양식')|(df['대분류']=='뷔페'),'대분류'] = '식사-양식'
df.loc[df['대분류']=='한식-육류,고기', '대분류'] = '육류/고기'
df.loc[df['대분류']=='한식-해물,생선','대분류']='식사-해물'
df.loc[df['대분류']=='패스트푸드','대분류']='식사-패스트푸드'
df.loc[df['대분류']=='중식','대분류']='식사-중식'
df.loc[df['대분류']=='일식','대분류']='식사-일식'
df.loc[df['대분류']=='술집','대분류']='주점/술집'
df.loc[df['대분류']=='분식','대분류']='식사-분식'

df.drop(columns=['분류', '세부분류'], inplace=True)
df.columns = ['이름', 'lon', 'lat', '대분류']

############################################################

# MAPBOX API / PYDECK
# CENTER POSITION
center = [['연희직업전문학교', 126.677211723637, 37.5428959487629]]
center_df = pd.DataFrame(center)
center_df.columns = ['이름', 'lon', 'lat']

# 메뉴 데이터
kind = df['대분류'].unique()
kind = sorted(kind)
# ['디저트/간식/샐러드', '식사-국밥/탕', '식사-면류', '식사-분식', '식사-양식', '식사-일식', '식사-중식', '식사-패스트푸드', '식사-한식/도시락', '식사-해물', '육류/고기', '주점/술집', '치킨']

# 디저트        url = https://cdn-icons-png.flaticon.com/512/4629/4629607.png
# 국밥          url = https://cdn-icons-png.flaticon.com/512/575/575511.png
# 국수          url = https://cdn-icons-png.flaticon.com/512/4629/4629545.png
# 분식          url = https://cdn-icons-png.flaticon.com/512/4629/4629733.png
# 양식          url = https://cdn-icons-png.flaticon.com/512/1869/1869100.png
# 일식          url = https://cdn-icons-png.flaticon.com/512/4629/4629532.png
# 중식          url = https://cdn-icons-png.flaticon.com/512/4161/4161307.png
# 패스트푸드    url = https://cdn-icons-png.flaticon.com/512/4629/4629522.png
# 한식/도시락   url = https://cdn-icons-png.flaticon.com/512/168/168559.png
# 해물          url = https://cdn-icons-png.flaticon.com/512/4629/4629669.png
# 육류/고기     url = https://cdn-icons-png.flaticon.com/512/4629/4629658.png
# 주점/술집     url = https://cdn-icons-png.flaticon.com/512/4629/4629700.png
# 치킨          url = https://cdn-icons-png.flaticon.com/512/4629/4629603.png

# ICON DATA
CENTER_ICON_URL = 'https://cdn-icons-png.flaticon.com/512/1344/1344761.png' # 학교 아이콘
center_icon_data = {
    "url": CENTER_ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
}

# ICON_URL = 'https://cdn-icons-png.flaticon.com/512/857/857718.png'
# icon_data = {
#     "url": ICON_URL,
#     "width": 242,
#     "height": 242,
#     "anchorY": 242,
# }

icon_data = [{#디저트
    "url": 'https://cdn-icons-png.flaticon.com/512/4629/4629607.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#국밥
    "url": 'https://cdn-icons-png.flaticon.com/512/575/575511.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#국수
    "url": 'https://cdn-icons-png.flaticon.com/512/4629/4629545.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#분식
    "url": 'https://cdn-icons-png.flaticon.com/512/4629/4629733.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#양식
    "url": 'https://cdn-icons-png.flaticon.com/512/1869/1869100.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#일식
    "url": 'https://cdn-icons-png.flaticon.com/512/4629/4629532.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#중식
    "url": 'https://cdn-icons-png.flaticon.com/512/4161/4161307.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#패스트푸드
    "url": 'https://cdn-icons-png.flaticon.com/512/4629/4629522.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#한식/도시락
    "url": 'https://cdn-icons-png.flaticon.com/512/168/168559.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#해물
    "url": 'https://cdn-icons-png.flaticon.com/512/4629/4629669.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#육류/고기
    "url": 'https://cdn-icons-png.flaticon.com/512/4629/4629658.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#주점/술집
    "url": 'https://cdn-icons-png.flaticon.com/512/4629/4629700.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
},
{#치킨
    "url": 'https://cdn-icons-png.flaticon.com/512/4629/4629603.png',
    "width": 242,
    "height": 242,
    "anchorY": 242,
}]

# DF에 아이콘 데이터 삽입
df['icon_data'] = None

# for i in df.index:
#     df['icon_data'][i] = icon_data[0]

df_set = df.copy()

for n in range(0,len(kind)):
    df_temp = df.loc[df['대분류']==kind[n]]
    for i in df_temp.index:
        df_temp['icon_data'][i] = icon_data[n]
    df_set=df_set.append(df_temp, ignore_index=True)
df_set.dropna(inplace=True)

del df

center_df['icon_data'] = None
center_df['icon_data'][0] = center_icon_data



# MAIN SCREEN
st.title('오늘 뭐 먹지?')
st.write('연희 직업전문학교를 중심으로 반경 내에 있는 식당을 찾아줍니다.')

# FILTERRING BY DISTANCE    # FEATURE-1
st. sidebar.markdown('### 거리별 필터')
df_set['x거리'] = abs (center[0][1]*100000 - df_set['lon']*100000)
df_set['y거리'] = abs (center[0][2]*100000 - df_set['lat']*100000)
df_set['distance'] = (df_set['x거리']**2 + df_set['y거리']**2)**0.5

distance = st.sidebar.slider('반경 (m)', min_value=0, max_value=700, value=200, step=10)
df_set = df_set.loc[df_set['distance'] <= distance,]


# STORE LAYERS CREATE
STORE_LAYERS = {}
for i in range(0,len(kind)):
    STORE_LAYERS[kind[i]] = pdk.Layer(
        'IconLayer',
        data=df_set.loc[df_set['대분류'] == kind[i],][['이름', 'lon', 'lat', 'icon_data']],
        get_icon='icon_data',
        get_size=4,
        size_scale=10,
        get_position=['lon', 'lat'],
        pickable=True
    )

# FILTERRING BY CATEGORIES  # FEATURE-2
st. sidebar.markdown('### 메뉴별 필터')

layers = st.sidebar.multiselect('', STORE_LAYERS.keys(), default = [kind[1], kind[7], kind[8]])#
selected_layers = [
    layer for layer_name, layer in STORE_LAYERS.items()
    if layer_name in layers]


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

# st.title('여긴 끝')
with st.expander("오늘은 어디까지 가볼까"):          
    st.write('**반경 150m 이내** : 여유롭게 식사하고 카페나 편의점도 들를 수 있습니다.')
    st.write('**반경 150m 바깥** : 길게 대화하기에는 어렵지만, 잠시 카페나 편의점을 들렀다 올 정도입니다.')
    st.write('**반경 300m 바깥** : 식사 외 용무가 있다면 조금 서두를 필요가 있습니다.')
    st.write('**반경 500m 바깥** : 제시간에 돌아오지 못할 수도 있습니다. 서둘러 식사만 마치고 오세요.')

with st.expander('범주와 아이콘', expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image (icon_data[0]['url'], caption=kind[0], width=80)
        st.image (icon_data[3]['url'], caption=kind[3], width=80)
        st.image (icon_data[6]['url'], caption=kind[6], width=80)
        st.image (icon_data[9]['url'], caption=kind[9], width=80)
        st.image (icon_data[12]['url'], caption=kind[12], width=80)

    with col2:
        st.image (icon_data[1]['url'], caption=kind[1], width=80)
        st.image (icon_data[4]['url'], caption=kind[4], width=80)
        st.image (icon_data[7]['url'], caption=kind[7], width=80)
        st.image (icon_data[10]['url'], caption=kind[10], width=80)
        
    with col3:
        st.image (icon_data[2]['url'], caption=kind[2], width=80)
        st.image (icon_data[5]['url'], caption=kind[5], width=80)
        st.image (icon_data[8]['url'], caption=kind[8], width=80)
        st.image (icon_data[11]['url'], caption=kind[11], width=80)

st.subheader('아이콘 이미지 라이선스')
st.write ('https://www.flaticon.com/')
st.markdown ('##### 아이콘 제작자')
st.markdown ('###### Freepik')
st.write ('https://www.freepik.com')
st.markdown ('###### DinosoftLabs')
st.write ('https://www.flaticon.com/kr/authors/dinosoftlabs')