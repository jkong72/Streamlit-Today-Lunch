import streamlit as st
from urllib import request
from urllib.request import Request, urlopen
from urllib import parse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
import pandas as pd

# from secure import kko_rest

# feature is not prepare

def point_search (keyword):
    req_url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=' #키워드 검색
    client_key = kko_rest()
    search = keyword
    size = 1
    
