from datetime import datetime
from urllib import request
import json
import time
import xmltodict
import requests
from bs4 import BeautifulSoup
from lib.lh_config import LH_web, label_list
from lib.etri_config import ETRI_web, key_list
from urllib.parse import quote_plus
import re


class G2B:
    query_retry = 50
    query_retry_time = 10
    fail_retry_time = 30
    timeout = 120

    sub_type = None

    def __init__(self, begin=None, end=None, filtering=None):
        self.begin = begin
        self.end = end
        self.filtering = filtering

    def set_query_url(self, url):
        self.url = url

    def set_query_sub_type(self, sub_type):
        self.sub_type = sub_type

    def set_page(self, page, rows):
        self.page = page
        self.rows = rows

    def get_result_code(self):
        try:
            self.result_code = int(self.json_data['response']['header']['resultCode'])
        except (KeyError, TypeError, ValueError) as e:
            self.logger.error(e)
            self.result_code = -1

    def get_total_count(self):
        try:
            self.total_count = int(self.json_data['response']['body']['totalCount'])
        except (KeyError, TypeError, ValueError) as e:
            self.logger.error(e)
            self.total_count = -1

    def calc_date(self, item):
        try:
            item_dt = item.get(self.filtering)
            if not item_dt:
                return False

            return datetime.strptime(item_dt, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M') < self.begin
        except ValueError:
            self.logger.error(f'item({item})')
            return False

    def list_calc_date(self, item):
        try:
            rgst_dt = item.get(self.filtering[0])
            chg_dt = item.get(self.filtering[1])

            if not rgst_dt and not chg_dt:
                return False
            elif not chg_dt:
                rgst_dt_str = datetime.strptime(rgst_dt, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M')
                return rgst_dt_str >= self.begin
            elif not rgst_dt:
                chg_dt_str = datetime.strptime(chg_dt, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M')
                return chg_dt_str >= self.begin
            else:
                rgst_dt_str = datetime.strptime(rgst_dt, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M')
                chg_dt_str = datetime.strptime(chg_dt, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M')
                return rgst_dt_str >= self.begin or (rgst_dt_str < self.begin and chg_dt_str >= self.begin)
        except ValueError:
            self.logger.error(f'item({item})')
            return False

    def query_page(self):
        self.get_total_count()
        (q, r) = divmod(self.total_count, self.rows)
        self.page_count = q if r == 0 else q + 1

    def query_data(self, type, retry=0):

        if(type < 3):
            if self.get_LH_query_data() is False:
                return False
        self.get_result_code()

        if self.result_code == 0:
            if self.page == 1:
                self.query_page()

            if (type < 3):
                return self.get_LH_items(type) if self.total_count > 0 else True
            elif(type > 3):
                return self.get_ETRI_items(type) if self.total_count > 0 else True
        elif self.result_code > 0 and self.result_code < 6:
            if retry >= self.query_retry:
                self.logger.info(f'max retry excced({retry})')
                return False

            time.sleep(self.fail_retry_time)

            self.logger.info(f'retry query({retry})')
            return self.query_data(retry + 1)
        elif self.result_code > 6:
            self.logger.info(f'response code error({self.result_code})')
            return False
        elif self.result_code == -1:
            self.logger.info(f'skip url({self.url}')
            return False
        else:
            self.logger.info(f'unknown response code({self.result_code})')
            return False

# common_API
    def strip_re(self, body):
        del_list = {'\r', '\n', '\t'}
        body = body.text.strip()
        for value in del_list:
            body = body.replace(value, '')
        return body

# LH_API
    def get_LH_items(self, type):
        try:
            self.r_item = self.json_data["response"]["body"]["item"]

            self.item_data = []

            for item in self.r_item:
                self.bidNum = item.get('bidNum')
                self.bidDegree = item.get('bidDegree')
                if type == 1:   # 입찰공고
                    item['입찰공고'] = self.get_LH_dict(LH_web.URL) # 파일명
                    item['입찰공고'].update(self.get_LH_dict_file())    # 파일 URL
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
                elif type == 2: # 개찰결과
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
            return True
        except KeyError as e:
            self.logger.error(e)
            return False
    # 웹 크롤링 데이터 가져오기
    def get_LH_dict(self, url): 
        temp_dict = {}
        url = url + self.bidNum + '&bidDegree=' + self.bidDegree
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            self.soup_obj = BeautifulSoup(html, 'html.parser')
        else:
            print(response.status_code)
        for i in range(1, 7):
            id_label1 = 'LblockDetail' + str(i)
            if (self.soup_obj.find('div', id=id_label1)) is not None:
                for value in self.soup_obj.find('div', id=id_label1).find_all('tr'):
                    label = value.find('th').find('label').text.strip()
                    data = value.find('td').text.strip()
                    if (label) in label_list:
                        temp_dict[label] = data
            else:
                break
        return temp_dict

    def get_LH_dict_file(self):
        # {'파일명': 'filename', 'URL': 'fileURL'} <- 저장
        temp_dict = {
            '첨부파일': []
            }
        for value in self.soup_obj.find('div', class_="LblockListTable").find_all('tr', class_='Lfirst'):
            temp = {}
            temp['파일명'] = value.find('a', class_='attach').text.strip()
            temp['URL'] = self.get_file_url(value.find('a', class_='attach')['href'])
            temp_dict['첨부파일'].append(temp)

        return temp_dict

    def get_file_url(self, ex_file):

        if (ex_file) == '':
            return ''

        temp = ex_file[23:-2].split('\',')

        if ((temp[1][0]) != '\''):
            print("savename error")
            return ''
        if ((temp[3][0] or temp[3][-1]) != '\''):
            print("filename error")
            return ''

        savename = temp[1][1:]
        filename = temp[3][1:-1]

        savename = quote_plus(savename)
        filename = quote_plus(filename)

        file_url = LH_web.file_url(savename, filename)
        return file_url

    #자체 api에서 가져오기
    def get_LH_query_data(self):
        for i in range(self.query_retry):
            try:
                with request.urlopen(self.url, timeout=self.timeout) as response:
                    result = response.read().decode('cp949')
                    dictionary = xmltodict.parse(result)        # JSON 으로 변환
                    json_object = json.dumps(dictionary)
                    self.json_data = json.loads(json_object)

                    return True
            except Exception as e:
                self.logger.error(e)
        return False

# ETRI_API
    def get_ETRI_cookie(self):
        response = requests.get(ETRI_web.URL)

        if response.status_code == 200:
            header = response.headers
            self.cookie = header['Set-Cookie']
            return True
        else:
            print(response.status_code)
            return False

    def get_etri_file(self, body):
        temp = re.search('\'.+\'', body['onclick']).group()[1:]
        temp = temp.replace('\'', '')
        temp = temp.replace(' ', '')
        temp = temp.split(',')
        url = f'{ETRI_web.D_URL}?file_id={temp[0]}&file_gb={temp[1]}'

        return url

    def get_ETRI_items(self, type):
        try:
            self.item_data = []
            if type == 3:   # 입찰공고
                item = self.get_ETRI_announce(self.url)
                self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
            elif type == 4: # 개찰결과
                item = self.get_ETRI_result(self.url)
                self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
            return True
        except KeyError as e:
            self.logger.error(e)
        return False

    def get_ETRI_announce(self, url):
        item_arr = []
        item_dic = {}
        temp_arr = []
        result_dic = {}

        # 쿠키 가져오기
        if self.get_ETRI_cookie() is False:
            return False

        # 쿠키 넣어주기
        header = {'Cookie': self.cookie}
        response = requests.get(url, headers=header)

        if response.status_code == 200:
            html = response.text
            self.soup_obj = BeautifulSoup(html, 'html.parser')
        else:
            print(response.status_code)

        if (self.soup_obj.find_all('table', id='table01')) is not None:
            i = 0
            for value in self.soup_obj.find_all('table', id='table01'):
                j = 0
                if (i == 0):    # 공고번호
                    item_arr = []
                    for body in value.find_all('td', class_='name02'):
                        item_arr.append(self.strip_re(body))
                    for body in value.find_all('td', class_=''):
                        if j >= 14:
                            if(j == 16):
                                temp_arr.append(self.strip_re(body))
                                result_dic[item_arr[14]] = {}
                                result_dic[item_arr[14]][item_arr[15]] = temp_arr
                                temp_arr = []
                            elif(j == 19):
                                temp_arr.append(self.strip_re(body))
                                result_dic[item_arr[14]][item_arr[16]] = temp_arr
                            else:
                                temp_arr.append(self.strip_re(body))
                            j += 1
                        else:
                            result_dic[item_arr[j]] = self.strip_re(body)
                            j += 1
                if(i == 1):     # 입찰 일정
                    j = 0
                    temp_arr = []
                    item_arr = []
                    item_dic = {}
                    result_dic['입찰일정'] = []
                    for body in value.find_all('td', class_='list01'):
                        temp_arr.append(self.strip_re(body))
                    for body in value.find_all('td', class_=''):
                        if(j == 5):
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            j = 0
                            item_arr.append(item_dic)
                            result_dic['입찰일정'].append(item_arr)
                            item_dic = {}
                            item_arr = []
                        else:
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            j += 1
                if(i == 2):     # 입찰참고사항
                    result_dic[value.find('td', class_='name02').text.strip()] = value.find('textarea').text.strip()
                if(i == 3):     # 가격정보
                    temp_arr = []
                    item_arr = []
                    item_dic = {}
                    result_dic['가격정보(단위:원)'] = {}
                    for body in value.find_all('td', class_='name02'):
                        temp_arr.append(self.strip_re(body))
                    for body in value.find_all('td', class_=''):
                        if(j == (len(temp_arr) - 1)):
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            result_dic['가격정보(단위:원)'] = item_dic
                        else:
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            j += 1
                if(i == 4):     # 입찰공고안내서류
                    j = 0
                    temp_arr = []
                    item_arr = []
                    item_dic = {}
                    result_dic['입찰공고안내서류'] = []
                    for body in value.find_all('td', class_='list01'):
                        temp_arr.append(self.strip_re(body))
                    for body in value.find_all('td', class_=''):
                        if(j == (len(temp_arr) - 1)):
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            item_dic['URL'] = self.get_etri_file(body.find('a'))
                            j = 0
                            item_arr.append(item_dic)
                            result_dic['입찰공고안내서류'].append(item_arr)
                            item_dic = {}
                            item_arr = []
                        else:
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            j += 1
                i += 1
        return result_dic

    def get_ETRI_result(self, url):
        item_arr = []
        item_dic = {}
        result_dic = {}
        # 쿠키 가져오기
        if self.get_ETRI_cookie() is False:
            return False

        # 쿠키 넣어주기
        header = {'Cookie': self.cookie}
        response = requests.get(url, headers=header)

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


