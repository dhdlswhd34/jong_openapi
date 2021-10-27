import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus
import re
from requests.models import Response
from datetime import datetime
import schedule
import time

def run():
    print('start'+str(datetime.now()))
    pagenum = '01'
    start = '20211001'
    end = '20211031'
    year = '2021'
    result_arr = []
    temp_arr = []
    list_arr = []
# 쿠키
    url = 'https://ebid.etri.re.kr/ebid/index.do'

    response = requests.get(url)

    header = response.headers

    cookie = header['Set-Cookie']

    headerr = {'Cookie': cookie}

# 웹 크롤링
    i=1
    while True:
        pagenum = i
        query = f'?pageNo={pagenum}&search=Y&sch_fromDate={start}&sch_toDate={end}' 
        # query = f'?pageNo={pagenum}&pageGb=C&search=Y&sch_fromDate={start}&sch_toDate={end}' 
        url = 'https://ebid.etri.re.kr/ebid/ebid/ebidEstmtRqstList.do' + query
        response_result = requests.get(url, headers=headerr)
        if response.status_code == 200:
            html = response_result.text
            soup_obj = BeautifulSoup(html, 'html.parser')
        else:
            print(response.status_code)

        temp = []

        j = 0
        for value in soup_obj.find('table', id='table01').find_all('tr'):
            for body in value.find_all('td'):
                if body.text.strip() == '자료가 존재하지 않습니다.':
                    i = -1
                    break
                temp = re.search(f'E.{year}.+\)', body.text.strip())
                temp_S = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', body.text.strip())
                if temp is not None:
                    # print(temp.group())
                    temp_arr.append(temp.group())
                if temp_S is not None:
                    # print(temp_S.group())
                    temp_arr.append(temp_S.group())
                j += 1
            if len(temp_arr) > 1:
                result_arr.append(temp_arr)
            temp_arr = []

        if(i == -1):
            print(url)
            break
        i+=1


    f = open('backup_list2.txt', 'rt' , encoding='UTF8')
    while True:
        line = f.readline()
        if not line:
            break
        line = line.split(',')
        list_arr.append(line)
    f.close()

    f = open('backup_list2.txt', 'a+', encoding='UTF8')
    for bs in result_arr:
        i = 1
        for txt in list_arr:
            if(txt[0:3] == bs):
                i = 0
                break
        if(i == 1):
            current_time = datetime.now()
            f.write(f'{bs[0]},{bs[1]},{bs[2]},{current_time}\n')
    f.close()


schedule.every(30).minutes.do(run)
# schedule.every(15).seconds.do(run)

if __name__ == '__main__':
    run()
    while True:
        schedule.run_pending()
    time.sleep(1)