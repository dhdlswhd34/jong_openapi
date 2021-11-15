from datetime import datetime
from urllib import request
import json
import time
import xmltodict
import requests
from bs4 import BeautifulSoup
from lib.logger import Logger
from lib.lh_config import LH_web, label_list
from lib.etri_config import ETRI_web
from lib.etri_config import announce_enum as an
from lib.etri_config import result_enum as rn
from lib.etri_config import ex_enum as en
from urllib.parse import quote_plus
from functools import reduce
import pandas as pd
import re
from lib.db import Db

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
        self.result_arr = []
        self.bidnum_degree = []
        self.page_check = 0

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
        del_list = ['\r', '\n', '\t']
        body = str(body).strip()
        return reduce(lambda src, filter: src.replace(filter, ''), del_list, body)

    def strip_re_w(self, body):
        del_list = ['\r', '\n', '\t']
        body = body.text.strip()
        return reduce(lambda src, filter: src.replace(filter, ''), del_list, body)

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

        for i in range(self.query_retry):
            if response.status_code == 200:
                html = response.text
                self.soup_obj = BeautifulSoup(html, 'html.parser')
            else:
                self.logger.error(response.status_code)
                continue
                
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
            self.logger.error("savename error")
            return ''
        if ((temp[3][0] or temp[3][-1]) != '\''):
            self.logger.error("filename error")
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
    # 쿠키 가져오기
    def get_ETRI_cookie(self):
        self.header = {}
        response = requests.get(ETRI_web.URL)

        if response.status_code == 200:
            header = response.headers
            self.cookie = header['Set-Cookie']
            self.header = {'Cookie': self.cookie}
            return True
        else:
            self.logger.error(response.status_code)
            return False

    # 첨부파일 가져오기
    def get_etri_file(self, body):
        temp = re.search('\'.+\'', body['onclick']).group()[1:]
        temp = reduce(lambda src, filter: src.replace(filter, ''), ['\'', ' '], temp)
        temp = temp.split(',')
        url = f'{ETRI_web.D_URL}?file_id={quote_plus(temp[0])}&file_gb={quote_plus(temp[1])}'
        return url

    def check_change_list(self, page):
        for last in self.result_arr[page-2]:
            for now in self.result_arr[page-1]:
                if last == now:
                    return False
        return True

    # 공고번호, 시작, 종료 리스트 목록 가져오기
    def get_ETRI_query_data(self, page, headerr, type):
        temp_arr = []
        # 3:입찰공고 4:개찰결과 5:견적문의 6:견적결과
        if(type == 3):
            query = f'?pageNo={page}&search=Y&sch_fromDate={self.begin}&sch_toDate={self.end}'
            url = ETRI_web.check_URL + query
        elif(type == 4):
            query = f'?pageNo={page}&pageGb=C&search=Y&sch_fromDate={self.begin}&sch_toDate={self.end}'
            url = ETRI_web.check_URL + query
        elif(type == 5):
            query = f'?pageNo={page}&search=Y&sch_fromDate={self.begin}&sch_toDate={self.end}'
            url = ETRI_web.cust_URL + query
        elif(type == 6):
            query = f'?pageNo={page}&search=Y&sch_fromDate={self.begin}&sch_toDate={self.end}'
            url = ETRI_web.cust_URL + query
            check = '진행'  # 진행 빼고 다

        for i in range(self.query_retry):
            try:
                with requests.get(url, headers=self.header) as response_result:
                    if response_result.status_code == 200:
                        html = response_result.text
                        soup_obj = BeautifulSoup(html, 'html.parser')
                    else:
                        continue

                    table = soup_obj.find('table', id='table01')
                    tables = pd.read_html(str(table))

                    print(url)

                    if(tables[0][0][1] == '자료가 존재하지 않습니다.'):
                        print('end')
                        return 'end'

                    if (type == 6):
                        for j in range(1, len(tables[0][0])):
                            if tables[0][6][j] != check:
                                temp_arr.append([tables[0][0][j], tables[0][3][j], tables[0][4][j], tables[0][6][j]])
                        if len(temp_arr) > 0:
                            self.result_arr.append(temp_arr)
                            self.page_check += 1
                    elif (type==3):
                        # 저장 (ex. [공고번호(차수), 입찰시작일, 입찰종료일, 진행상태])
                        self.result_arr.append([[tables[0][1][j], tables[0][4][j], tables[0][5][j], tables[0][7][j]] for j in range(1, len(tables[0][0]))])
                        self.page_check += 1
                    else:
                        # 저장 (ex. [공고번호(차수), 입찰시작일, 입찰종료일, 진행상태])
                        self.result_arr.append([[tables[0][0][j], tables[0][3][j], tables[0][4][j], tables[0][6][j]] for j in range(1, len(tables[0][0]))])
                        self.page_check += 1

                    # 새로들어온 리스트 체크
                    if  self.page_check > 2:
                        if self.check_change_list(self.page_check) is False:
                            return 'back'
                    return True
            except Exception as e:
                self.logger.error(e)
        return False

    # 데이터 크롤링
    def get_ETRI_items(self, type):
        try:
            self.item_data = []
            for bidnum_degree in self.bidnum_degree:
                url = f'{self.url}?biNo={bidnum_degree[0]}'     # URL 설정
                print(url)
                if type == 3:   # 입찰공고
                    item = self.get_ETRI_announce(url)
                    item.update(self.get_ETRI_ex_info(ETRI_web.ex_info_URL,bidnum_degree[0]))   # 추가 탭 데이터 가져오기
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
                elif type == 4:  # 개찰결과
                    item = self.get_ETRI_result(url)
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
                elif type == 5:  # 견적요청
                    item = self.get_ETRI_announce(url)
                    item.update(self.get_ETRI_ex_info(ETRI_web.ex_info_URL,bidnum_degree[0]))   # 추가 탭 데이터 가져오기
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
                elif type == 6:  # 견적요청
                    item = self.get_ETRI_result(url)
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
            return True
        except KeyError as e:
            self.logger.error(e)
        return False

    # 첨부파일
    def exfile_cw(self, count):
        temp_arr = []
        # url 가져오기
        url_arr = [self.get_etri_file(file) for file in self.table[-1].find_all('a')]
        for i in range(1, len(self.tables[count].index)):
            item_dic = {}
            for j in range(0, len(self.tables[count].columns)):
                item_dic[self.tables[count][j][0]] = self.tables[count][j][i]
            item_dic['URL'] = url_arr[i-1]
            temp_arr.append(item_dic)

        return temp_arr

    # 테이블 번호, 결과, 시작값, 열개수 
    def liner_cw(self, count, start, row, ex):
        item_dic = {}
        for i in range(ex, len(self.tables[count].index)):
            for j in range(start, start + row):
                item_dic[self.strip_re(self.tables[count][(j*2)][i])] = self.strip_re(self.tables[count][(j*2)+1][i])
        return item_dic

    def columns_cw(self, count):
        temp_arr = []
        for i in range(1, len(self.tables[count].index)):
            item_dic = {}
            for j in range(0, len(self.tables[count].columns)):
                item_dic[self.tables[count][j][0]] = self.tables[count][j][i]
            temp_arr.append(item_dic)
        return temp_arr

    def get_ETRI_announce(self, url):
        result_dic = {}
        item_dic = {}
        # 쿠키 가져오기
        for i in range(self.query_retry):
            if self.get_ETRI_cookie() is False:
                sleep(self.timeout)
                continue

            response = requests.get(url, headers=self.header)

            if response.status_code == 200:
                html = response.text
                self.soup_obj = BeautifulSoup(html, 'html.parser')
            else:
                self.logger.error(response.status_code)
                sleep(self.timeout)
                continue

            self.table = self.soup_obj.find_all('table', id='table01')
            self.tables = pd.read_html(str(self.table))
            #nan제거
            for i in range(0, len(self.tables)):
                self.tables[i] = self.tables[i].fillna('')

            t_len = len(self.tables[0])

            # 공고번호
            for i in range(0, len(self.tables[0][0]) - 2):
                result_dic[self.strip_re(self.tables[0][0][i])] = self.strip_re(self.tables[0][1][i])
                result_dic[self.strip_re(self.tables[0][3][i])] = self.strip_re(self.tables[0][4][i])

            item_dic[self.strip_re(self.tables[0][1][t_len-2])] = [self.strip_re(self.tables[0][2][t_len-2]), self.strip_re(self.tables[0][3][t_len-2]), self.strip_re(self.tables[0][4][t_len-2])]
            item_dic[self.strip_re(self.tables[0][1][t_len-1])] = [self.strip_re(self.tables[0][2][t_len-1]), self.strip_re(self.tables[0][3][t_len-1]), self.strip_re(self.tables[0][4][t_len-1])]
            result_dic[self.strip_re(self.tables[0][0][t_len-1])] = item_dic

            # 입찰일정
            result_dic['입찰일정'] = self.columns_cw(1)

            # 입찰참고사항
            result_dic[self.strip_re(self.tables[2][0][0])] = self.strip_re(self.tables[2][1][0])

            # 가격정보
            result_dic['가격정보'] = self.liner_cw(3, 0, 2, 0)
        
            if (len(self.tables)) > 5:
                # 적격심사 세부기준
                result_dic['적격심사세부기준'] = self.liner_cw(4, 0, 2, 0)
                # 첨부파일
                result_dic['입찰공고안내서류'] = self.exfile_cw(5)
            elif(len(self.tables)) <= 5:
                # 첨부파일
                result_dic['입찰공고안내서류'] = self.exfile_cw(4)

            return result_dic

    def get_ETRI_result(self, url):
        result_dic = {}
        # 쿠키 가져오기
        for i in range(self.query_retry):
            if self.get_ETRI_cookie() is False:
                sleep(self.timeout)
                continue

            # 쿠키 넣어주기
            response = requests.get(url, headers=self.header)

            if response.status_code == 200:
                html = response.text
                self.soup_obj = BeautifulSoup(html, 'html.parser')
            else:
                self.logger.error(response.status_code)
                sleep(self.timeout)
                continue                

            table = self.soup_obj.find_all('table', id='table01')
            self.tables = pd.read_html(str(table))

            #nan제거
            for i in range(0, len(self.tables)):
                self.tables[i] = self.tables[i].fillna('')

            # 최종결과
            result_dic['최종결과'] = self.liner_cw(1, 0, 2, 0)
            if(len(self.tables) > 2):
                # 복수 예비가격 및 예정가격
                if(len(self.tables) == 3):
                    # 개찰결과
                    result_dic['개찰결과'] = self.columns_cw(2)
                else:
                    result_dic['복수예비가격'] = self.liner_cw(2, 0, 3, 1)

                    result_dic['추첨결과 및 예정결과'] = self.liner_cw(2, 3, 1, 1)

                    # 개찰결과
                    result_dic['개찰결과'] = self.columns_cw(3)

            return result_dic


    # 추가 탭 (입찰내역 가져오기)
    def get_ETRI_ex_info(self, url, bidnum_degree):

        for i in range(self.query_retry):
            # 쿠키 가져오기
            if self.get_ETRI_cookie() is False:
                sleep(self.timeout)
                continue                

            url = url + f'?biNo={bidnum_degree}'    # URL이 달라 따로 설정
            # 쿠키 넣어주기
            response = requests.get(url, headers=self.header)

            if response.status_code == 200:
                html = response.text
                self.soup_obj = BeautifulSoup(html, 'html.parser')
            else:
                self.logger.error(response.status_code)
                sleep(self.timeout)
                continue                

            if (self.soup_obj.find('table', id='table01')) is not None:
                result_dic = {}
                i = 0
                for value in self.soup_obj.find_all('table', id='table01'):
                    j = 0
                    temp_arr = []
                    item_arr = []
                    item_dic = {}
                    if(i == en.물품내역):     # 물품내역
                        result_dic['물품내역'] = []
                        # key값 가져오기
                        for body in value.find_all('td', class_='list01'):
                            if(self.strip_re_w(body) == '물품명세'):    # 물품 명세에서 끊기
                                temp_arr.append(self.strip_re_w(body))
                                break
                            temp_arr.append(self.strip_re_w(body))
                        # value 값 가져오기
                        for body in value.find_all('td', class_=''):
                            if(j == len(temp_arr)-1):
                                item_dic[temp_arr[j]] = self.strip_re_w(body)
                                j = 0
                                item_arr.append(item_dic)
                                result_dic['물품내역'].append(item_arr)
                                item_dic = {}
                                item_arr = []
                            else:
                                item_dic[temp_arr[j]] = self.strip_re_w(body)
                                j += 1
                    i += 1
            else:
                return False
            return result_dic
