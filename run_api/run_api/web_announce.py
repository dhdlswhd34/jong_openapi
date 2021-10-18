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

def get_etri_file(body):
    temp = re.search('\'.+\'', body['onclick']).group()[1:]
    temp = temp.replace('\'', '')
    temp = temp.replace(' ', '')
    temp = temp.split(',')
    url = f'https://ebid.etri.re.kr/ebid/download.do?file_id={temp[0]}&file_gb={temp[1]}'

    return url

if __name__ == '__main__':
    item_arr = []
    item_dic = {}
    temp = ''
    temp2 = ''
    temp_arr = []

    result_dic = {}
    bidnum = 'EA20212948'
    degree = '01'
    query = f'?biNo={bidnum}({degree})'

    url = 'https://ebid.etri.re.kr/ebid/index.do'

    response = requests.get(url)

    header = response.headers

    cookie = header['Set-Cookie']

    headerr = {'Cookie': cookie}
    url = 'https://ebid.etri.re.kr/ebid/ebid/ebidCustInfoMainView.do' + query
    response_result = requests.get(url, headers=headerr)
    if response.status_code == 200:
        html = response_result.text
        soup_obj = BeautifulSoup(html, 'html.parser')
    else:
        print(response.status_code)

    i = 0
    for value in soup_obj.find_all('table', id='table01'):
        j = 0
        if (i == 0):
            item_arr = []
            for body in value.find_all('td', class_='name02'):
                item_arr.append(strip_re(body))
            for body in value.find_all('td', class_=''):
                if j >= 14:
                    if(j == 16):
                        temp_arr.append(strip_re(body))
                        result_dic[item_arr[14]] = {}
                        result_dic[item_arr[14]][item_arr[15]] = temp_arr
                        temp_arr = []
                    elif(j == 19):
                        temp_arr.append(strip_re(body))
                        result_dic[item_arr[14]][item_arr[16]] = temp_arr
                    else:
                        temp_arr.append(strip_re(body))
                    j += 1
                else:
                    result_dic[item_arr[j]] = strip_re(body)
                    j += 1
        if(i == 1):
            j = 0
            temp_arr = []
            item_arr = []
            item_dic = {}
            result_dic['입찰일정'] = []
            for body in value.find_all('td', class_='list01'):
                temp_arr.append(strip_re(body))
            for body in value.find_all('td', class_=''):
                if(j == 5):
                    item_dic[temp_arr[j]] = strip_re(body)
                    j = 0
                    item_arr.append(item_dic)
                    result_dic['입찰일정'].append(item_arr)
                    item_dic = {}
                    item_arr = []
                else:
                    item_dic[temp_arr[j]] = strip_re(body)
                    j += 1
        if(i == 2):
            result_dic[value.find('td', class_='name02').text.strip()] = value.find('textarea').text.strip()
        if(i == 3):
            temp_arr = []
            item_arr = []
            item_dic = {}
            result_dic['가격정보(단위:원)'] = {}
            for body in value.find_all('td', class_='name02'):
                temp_arr.append(strip_re(body))
            for body in value.find_all('td', class_=''):
                if(j == (len(temp_arr) - 1)):
                    item_dic[temp_arr[j]] = strip_re(body)
                    result_dic['가격정보(단위:원)'] = item_dic
                else:
                    item_dic[temp_arr[j]] = strip_re(body)
                    j += 1
        if(i == 4):
            j = 0
            temp_arr = []
            item_arr = []
            item_dic = {}
            result_dic['입찰공고안내서류'] = []
            for body in value.find_all('td', class_='list01'):
                temp_arr.append(strip_re(body))
            for body in value.find_all('td', class_=''):
                if(j == (len(temp_arr) - 1)):
                    item_dic[temp_arr[j]] = strip_re(body)
                    item_dic['URL'] = get_etri_file(body.find('a'))
                    j = 0
                    item_arr.append(item_dic)
                    result_dic['입찰공고안내서류'].append(item_arr)
                    item_dic = {}
                    item_arr = []
                else:
                    item_dic[temp_arr[j]] = strip_re(body)
                    j += 1
        i += 1
    print(url)
    print(result_dic)
