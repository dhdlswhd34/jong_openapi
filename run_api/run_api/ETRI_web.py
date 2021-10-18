import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus
import re
from requests.models import Response


if __name__ == '__main__':

    result_dic = {}
    pagenum = '01'
    start = '20211015'
    end = '20211018'
    query = f'?pageNo={pagenum}&search=Y&sch_fromDate={start}&sch_toDate={end}'

# 쿠키
    url = 'https://ebid.etri.re.kr/ebid/index.do'

    response = requests.get(url)

    header = response.headers

    cookie = header['Set-Cookie']

    headerr = {'Cookie': cookie}

# 웹 크롤링
    url = 'https://ebid.etri.re.kr/ebid/ebid/ebidCustProgressList.do' + query

    response_result = requests.get(url, headers=headerr)
    if response.status_code == 200:
        html = response_result.text
        soup_obj = BeautifulSoup(html, 'html.parser')
    else:
        print(response.status_code)

    temp = []
    for value in soup_obj.find('table', id='table01').find_all('tr'):
        temp = re.search('EA.+\)', value.text.strip())
        if temp is not None:
            print(temp.group())

    print(url)
    print(temp)

    


    