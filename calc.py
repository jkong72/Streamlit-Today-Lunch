#########
#   -   #
# + c - #
#   +   #
#########

# 전체 범위 (여기서 선언한 변수는 기본적으로 고정됨)
from secure import kko_rest


cen_x =126.677211723637
cen_y =37.5428959487629
exa_x1 = cen_x-0.005
exa_x2 = cen_x+0.005
exa_y1 = cen_y+0.005
exa_y2 = cen_y-0.005

# 변수 설정
x1 = exa_x1
x2 = exa_x2
y1 = exa_y1
y2 = exa_y2

# 전체 사각형의 범위 리스트
rec_whole = [x1, y1, x2, y2]

# 거리
xhp = abs((x1-x2)/2) #x_half_point
yhp = abs((y1-y2)/2) #y_half_point
xhp = round(xhp, 3)
yhp = round(xhp, 3)

# 새로 얻어낸 등분 좌표
xh = x1+xhp
yh = y1-yhp

# 사분면
rec1 = [xh, y1, x2, yh]
rec2 = [x1, y1, xh, yh]
rec3 = [xh, y1, x2, yh]
rec4 = [xh, yh ,x2, y2]

# 하위 사분면 변수설정 (이하반복)
x1 = rec1[0]
y1 = rec1[1]
x2 = rec1[2]
y2 = rec1[3]


print (cen_x == xh)
print (cen_y == yh)
##############################

상위 범위 request
is_end = response['meta']['is_end']
total_count = response['meta']['total_count']

while total_count > 45:
    xhp = abs((x1-x2)/2) #x_half_point
    yhp = abs((y1-y2)/2) #y_half_point
    xhp = round(xhp, 3)
    yhp = round(xhp, 3)

    xh = x1+xhp
    yh = y1-yhp

    rec1 = [xh, y1, x2, yh]
    rec2 = [x1, y1, xh, yh]
    rec3 = [xh, y1, x2, yh]
    rec4 = [xh, yh ,x2, y2]

    rec1 = 
    return = [total_count, df]

else:
    df.append 
    

if is_end == True :
    break



def store_search (x1, y1, x2, y2):
    resp_list =[]
    page = 1
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

        url = req_url+search+rect+page

        get = Request(url)
        get.add_header('Authorization', 'KakaoAK '+client_key)

        response = urlopen(get)
        response_body = response.read().decode('utf-8')
        response_body = json.loads(response_body) #JSON

        is_end = response_body['meta']['is_end']
        total_count = response_body['meta']['total_count']

        if total_count > 45 :
            resp_list.extend(store_search (xh, y1, x2, yh)) #rec1
            resp_list.extend(store_search (x1, y1, xh, yh)) #rec2
            resp_list.extend(store_search (xh, y1, x2, yh)) #rec3
            resp_list.extend(store_search (xh, yh ,x2, y2)) #rec4
            return resp_list
        else:
            if is_end ==False:
                page = page+1
                return resp_list.extend(response_body['documents'])
            else:
                return resp_list.extend(response_body['documents'])
