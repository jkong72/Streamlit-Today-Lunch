import streamlit as st
from urllib import request
from urllib.request import Request, urlopen
from urllib import parse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
import pandas as pd

# from secure import kko_rest

def store_search (x1, y1, x2, y2):
    df = pd.DataFrame(index=range(0,1), columns=['분류', '이름', 'x', 'y'])
    num = 1
    x1 = round(x1,3)
    y1 = round(y1,3)
    x2 = round(x2,3)
    y2 = round(y2,3)
    while True:
        xhp = abs((x1-x2)/2) #x_half_point
        yhp = abs((y1-y2)/2) #y_half_point
        xhp = round(xhp, 3)
        yhp = round(xhp, 3)

        xh = x1+xhp
        yh = y1-yhp

        req_url = 'https://dapi.kakao.com/v2/local/search/category.json?category_group_code='
        client_key = kko_rest() #REST API
        search = 'FD6'
        rect = f'&rect={x1},{y1},{x2},{y2}'
        page = f'&page={num}'

        url = req_url+search+rect+page

        print (f'{x1},{y1} 부터 {x2},{y2} 까지의 범위를 계산합니다.')
        get = Request(url)
        get.add_header('Authorization', 'KakaoAK '+client_key)

        response = urlopen(get)
        response_body = response.read().decode('utf-8')
        response_body = json.loads(response_body) #JSON

        is_end = response_body['meta']['is_end']
        total_count = response_body['meta']['total_count']

        if response_body['documents'] == []:
            print ('-'*15)
            print (url)
            print (response_body)
            print ('구성요소가 없습니다. 검색값을 확인바랍니다.')
            print ('-' * 15)
            break

        if total_count > 45 :
            print ('검색 결과가 너무 많습니다.')
            print ('사분면을 나눠 새로 계산합니다.')
            df = df.append(store_search (xh, y1, x2, yh), ignore_index=True) #rec1
            print (f'{xh},{y1} 부터 {x2},{yh} 범위의 계산을 끝냈습니다.')

            df = df.append(store_search (x1, y1, xh, yh), ignore_index=True) #rec2
            print (f'{x1},{y1} 부터 {xh},{yh} 범위의 계산을 끝냈습니다.')

            df = df.append(store_search (x1, yh, xh, y2), ignore_index=True) #rec3
            print (f'{x1},{yh} 부터 {xh},{y2} 범위의 계산을 끝냈습니다.')

            df = df.append(store_search (xh, yh ,x2, y2), ignore_index=True) #rec4
            print (f'{xh},{yh} 부터 {x2},{y2} 범위의 계산을 끝냈습니다.')
            print ('현재 범위 내의 사분면의 계산을 마쳤습니다.')
            print (df)
            return df
        else:
            if is_end ==False:
                num = num+1
                length = len(response_body['documents'])
                for i in range(0,length):
                    dic = {df.columns[0]:(response_body['documents'][i]['category_name']),
                    df.columns[1]:(response_body['documents'][i]['place_name']),
                    df.columns[2]:(response_body['documents'][i]['x'] ),
                    df.columns[3]:(response_body['documents'][i]['y'] )
                    }
                    df = df.append(dic, ignore_index=True)
                print (df)
                return df
            else:
                length = len(response_body['documents'])
                for i in range(0,length):
                    dic = {df.columns[0]:(response_body['documents'][i]['category_name']),
                    df.columns[1]:(response_body['documents'][i]['place_name']),
                    df.columns[2]:(response_body['documents'][i]['x'] ),
                    df.columns[3]:(response_body['documents'][i]['y'] )
                    }
                    df = df.append(dic, ignore_index=True)
                print (df)
                return df



cen_x =126.677211723637
cen_y =37.5428959487629
x1 = cen_x-0.005 #
x2 = cen_x+0.005 #
y1 = cen_y+0.005 #
y2 = cen_y-0.005 #
# 직접 실행
df = store_search (x1, y1, x2, y2)
print ('함수 실행 결과')
print (df)
df.to_csv('data/restaurant.csv', index=False)