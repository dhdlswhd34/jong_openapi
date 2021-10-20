import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus
import re
from requests.models import Response


def strip_re(body):
    del_list = {'\r', '\n', '\t'}
    body = body.text.strip()
    for value in del_list:
        body = body.replace(value, '')
    return body

def get_etri_dic(key_list, body):
    item_dic = {}
    item_dic[key_list[j]] = body.text.strip()
    return item_dic

if __name__ == '__main__':
    item_arr = []
    item_dic = {}
    result_dic = {}
    pagenum = '01'
    start = '20211015'
    end = '20211018'
    bidnum_degree = []

    key_list = ['No', '사업자번호', '업체명', '대표자', '입찰금액', '투찰율', '추첨번호', '입찰일시', '비고']

# 쿠키
    url = 'https://ebid.etri.re.kr/ebid/index.do'

    response = requests.get(url)

    header = response.headers

    cookie = header['Set-Cookie']

    headerr = {'Cookie': cookie}
    
# 웹 크롤링
    query = f'?pageNo={pagenum}&search=Y&sch_fromDate={start}&sch_toDate={end}'
    url = 'https://ebid.etri.re.kr/ebid/ebid/ebidCustProgressList.do' + query

    response_result = requests.get(url, headers=headerr)
    if response.status_code == 200:
        html = response_result.text
        soup_obj = BeautifulSoup(html, 'html.parser')
    else:
        print(response.status_code)

    temp_bid = []
    for value in soup_obj.find('table', id='table01').find_all('tr'):
        temp_bid = re.search('E.2021+\)', value.text.strip())
        if temp_bid is not None:
            bidnum_degree.append(temp_bid.group())

    print(bidnum_degree)

    for query_data in bidnum_degree:
        query = f'?biNo={query_data}'

        url = 'https://ebid.etri.re.kr/ebid/ebid/ebidCustInfoResultView.do' + query
        response_result = requests.get(url, headers=headerr)

        if response.status_code == 200:
            html = response_result.text
            soup_obj = BeautifulSoup(html, 'html.parser')
        else:
            print(response.status_code)

        result_dic = {}
        i = 0
        for value in soup_obj.find_all('table', id='table01'):
            j = 0
            if (i == 1):
                for body in value.find_all('td'):
                    # print(result_dic)
                    if j == 0:
                        temp = body.text.strip()
                        j = 1
                    else:
                        result_dic[temp] = body.text.strip()
                        j = 0
            elif (i == 2):
                for body in value.find_all('tr'):
                    if j == 0:
                        for item in body.find_all('td'):
                            result_dic[item.text.strip()] = []
                        j = 1
                    elif j == 1:
                        for item in body.find_all('td')[0:-1]:
                            result_dic['복수예비가격'].append(item.text.strip())
                            # result_dic[item.text.strip()] = {}
                        item_arr.append(body.find_all('td', class_='list01')[0].text.strip())
                        item_arr.append(body.find_all('td', class_='list01')[-1].text.strip())
                        result_dic['추첨결과 및 예정가격'].append(item_arr)
                        item_arr = []
            elif (i == 3):
                temp_arr = []
                item_arr = []
                item_dic = {}
                result_dic['개찰결과'] = []
                for body in value.find_all('td', class_ ='list01'):
                    temp_arr.append(strip_re(body))
                for body in value.find_all('td', class_=''):
                    if (j == (len(temp_arr) - 1)):
                        item_dic[temp_arr[j]] = strip_re(body)
                        j = 0
                        item_arr.append(item_dic)
                        result_dic['개찰결과'].append(item_arr)
                        item_dic = {}
                        item_arr = []
                    else:
                        item_dic[temp_arr[j]] = strip_re(body)
                        j += 1
            i += 1

        print(result_dic)
        print(url)