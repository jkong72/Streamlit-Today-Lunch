# 라이브러리 가져오기
import streamlit as st
from urllib.request import Request, urlopen
from urllib import parse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json

from secure import ncp
# 내부 패키지 가져오기


########################################
########## 실행 코드 ####################
########################################

########## API 인증 ####################
client_id = ncp()[0]
client_pw = ncp()[1]

# api_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode'
api_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=' # 검색 부분
search = '서울특별시 마포구 성산동 20-12'
search = parse.quote(search)
print('-' *12)
print(search)
url = api_url + search
print(url)
print('-' *12)
##########

# response.status_code # 200 is normal
reque = Request(url)
reque.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
reque.add_header('X-NCP-APIGW-API-KEY', client_pw)

response = urlopen(reque)
rescode = response.getcode()
if rescode == 200:
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)
    print (response_body)