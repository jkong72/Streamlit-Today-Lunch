import streamlit as st
from urllib import request
from urllib.request import Request, urlopen
from urllib import parse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
import pandas as pd

from secure import kko_rest

def raw_df():

    # req_url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' #주소 검색
    # req_url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=' #키워드 검색

    req_url = 'https://dapi.kakao.com/v2/local/search/category.json?category_group_code='
    client_key = kko_rest() #REST API
    search = 'FD6'
    # search = parse.quote(search) #문자열을 URL코드로
    center_x = '&x=126.677211723637' # 연희직업전문학교 x
    center_y = '&y=37.5428959487629' # 연희직업전문학교 y
    radius = '&radius=500' # 반경 500m #150, 300, 500 
    size = '&size=45' # 최대 45 # 시행결과 최대값은 15로, 매뉴얼의 오기인듯. 기본값이 최대값으로 되어 있음.

    # radius대신 rect를 이용한 사분면 전략으로 대체. (더 많은 검색 결과값을 얻기 위함.)

    #########
    #   -   #
    # + c - #
    #   +   #
    #########
    
    cen_x =126.677211723637
    cen_y =37.5428959487629
    x1 = cen_x-0.005
    x2 = cen_x+0.005
    y1 = cen_y+0.005
    y2 = cen_y-0.005

    xhp = abs((x1-x2)/2) #x_half_point
    yhp = abs((y1-y2)/2) #y_half_point

    xh = x1


    
    rec1 = [126.672, 37.548, 126.677, 37.543]
    rec2 = [126.677, 37.548, 126.682, 37.543]
    rec3 = [126.672, 37.543, 126.677, 37.538]
    rec4 = [126.677, 37.543, 126.682, 37.538]
    rec = [rec1, rec2, rec3, rec4]
    
    rect = f'&rect={rec2[0]},{rec2[1]},{rec2[2]},{rec2[3]}'
    
    pages = range(1,4+1)

    df = pd.DataFrame(index=range(0,1), columns=['분류', '이름', 'x', 'y'])

    #####
    page = '&page=1'
    url = req_url+search+rect+page

    get = Request(url)
    get.add_header('Authorization', 'KakaoAK '+client_key)

    response = urlopen(get)
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body) #JSON
    restaurant = response_body

    print (url)
    print (restaurant)

    length = len(restaurant['documents'])
    for i in range(0,length):
        dic = {df.columns[0]:(restaurant['documents'][i]['category_name']),
        df.columns[1]:(restaurant['documents'][i]['place_name']),
        df.columns[2]:(restaurant['documents'][i]['x'] ),
        df.columns[3]:(restaurant['documents'][i]['y'] )
        }
        df = df.append(dic, ignore_index=True)

    df.to_csv('data/restaurant.csv', index=False)
    #####


    # for num in pages :
    #     page = f'&page={num}'
    #     # page = '&page=4'
    #     url = req_url+search+rect+page

    #     get = Request(url)
    #     get.add_header('Authorization', 'KakaoAK '+client_key)

    #     response = urlopen(get)
    #     response_body = response.read().decode('utf-8')
    #     response_body = json.loads(response_body) #JSON
    #     restaurant = response_body
    #     # globals()['geo_json_page_{}'.format(pages.index(num)+1)] = response_body
    #     # vsc에서 globals() 함수를 통해 설정한 동적변수는 코드의 종료와 함께 사라진다.
    #     # 코드 작성중에는 메모리에 올라가 있지 않고, 코드의 실행이 끝나도 사라지니 자동완성이 불가능하다.
    #     # 단, 코드 내에서 실사용은 가능함.
    #     # 사실 이는 다른 변수들과 동일하나 변수마다 직접 선언하는 과정(=)이 생략되어서 그렇다.
    #     # 코드를 실행하기 전부터도 변수가 선언되면 자동완성하고 가져올 수 있다는점이 그 증거.
    #     # 그렇다면 동적변수로 불러온 후, 합치는 대신 불러올 때 바로 데이터 프레임으로 변환하면 더 좋겠다.
        
    #     length = len(restaurant['documents'])
    #     for i in range(0,length):
    #         dic = {df.columns[0]:(restaurant['documents'][i]['category_name']),
    #         df.columns[1]:(restaurant['documents'][i]['place_name']),
    #         df.columns[2]:(restaurant['documents'][i]['x'] ),
    #         df.columns[3]:(restaurant['documents'][i]['y'] )
    #         }
    #         df = df.append(dic, ignore_index=True)

    #     df.to_csv('data/restaurant.csv', index=False)


# 자체적으로 기동
raw_df()