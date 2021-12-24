from urllib import request
import streamlit as st
from urllib.request import Request, urlopen
from urllib import parse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json

from secure import noa

# 필요 정보
client_id = noa()[0]
client_pw = noa()[1]
req_url = 'https://openapi.naver.com/v1/search/local.json?query='

search = '서구청역 근처 음식점'
search = parse.quote(search)

dis_num = 10
display = f'&display={dis_num}'

url = req_url+search+display

# 리퀘스트
get = Request(url)
get.add_header('X-Naver-Client-Id', client_id)
get.add_header('X-Naver-Client-Secret', client_pw)

# 리스폰스
response = urlopen(get)
response_body = response.read().decode('utf-8')
response_body = json.loads(response_body) #JSON

# 최초 데이터
# print (response_body)

full_data = response_body
print (full_data)


# full_data['lastBuildDate']+'에 마지막으로 확인함.' #빌드데이트

# full_data['items'][n]['title'] #식당 이름
# '음식점' in full_data['items'][n]['category'] #음식점인지 (데이터 걸러낼때)
# full_data['items'][n]['category'] #식당 종류
# full_data['items'][n]['address'] #식당 주소
