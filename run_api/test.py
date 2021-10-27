import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus
import re
from requests.models import Response
from datetime import datetime
import schedule
import time


def get_ETRI_cust(self, url):
    item_arr = []
    item_dic = {}
    result_dic = {}

    url = 'https://ebid.etri.re.kr/ebid/index.do'

    response = requests.get(url)

    header = response.headers

    cookie = header['Set-Cookie']

    headerr = {'Cookie': cookie}

    response = requests.get(url, headers=headerr)

    if response.status_code == 200:
        html = response.text
        self.soup_obj = BeautifulSoup(html, 'html.parser')
    else:
        print(response.status_code)

    if (self.soup_obj.find('table', id='table01')) is not None:
        result_dic = {}
        i = 0
        for value in self.soup_obj.find_all('table', id='table01'):
            j = 0
            if (i == 1):
                for body in value.find_all('td'):
                    if j == 0:
                        temp = self.strip_re(body)
                        j = 1
                    else:
                        result_dic[temp] = self.strip_re(body)
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
                    temp_arr.append(self.strip_re(body))
                for body in value.find_all('td', class_=''):
                    if (j == (len(temp_arr) - 1)):
                        item_dic[temp_arr[j]] = self.strip_re(body)
                        j = 0
                        item_arr.append(item_dic)
                        result_dic['개찰결과'].append(item_arr)
                        item_dic = {}
                        item_arr = []
                    else:
                        item_dic[temp_arr[j]] = self.strip_re(body)
                        j += 1
            i += 1
    else:
        return False

    return result_dic


def run():
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
                # temp_S = re.search(f'{year}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', body.text.strip())
                temp_S = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', body.text.strip())
                if temp is not None:
                    print(temp.group())
                    temp_arr.append(temp.group())
                if temp_S is not None:
                    print(temp_S.group())
                    temp_arr.append(temp_S.group())
                j += 1
            if len(temp_arr) > 1:
                result_arr.append(temp_arr)
            temp_arr = []
        break
        if(i == -1):
            break
        i+=1
    print(result_arr)
    print(url)













if __name__ == '__main__':
    run()
    # while True:
    #     schedule.run_pending()
    # time.sleep(1)
