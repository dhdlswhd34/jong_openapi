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
                if type == 1:   # ????????????
                    item['????????????'] = self.get_LH_dict(LH_web.URL) # ?????????
                    item['????????????'].update(self.get_LH_dict_file())    # ?????? URL
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
                elif type == 2: # ????????????
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
            return True
        except KeyError as e:
            self.logger.error(e)
            return False
    # ??? ????????? ????????? ????????????
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
        # {'?????????': 'filename', 'URL': 'fileURL'} <- ??????
        temp_dict = {
            '????????????': []
            }
        for value in self.soup_obj.find('div', class_="LblockListTable").find_all('tr', class_='Lfirst'):
            temp = {}
            temp['?????????'] = value.find('a', class_='attach').text.strip()
            temp['URL'] = self.get_file_url(value.find('a', class_='attach')['href'])
            temp_dict['????????????'].append(temp)

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

    #?????? api?????? ????????????
    def get_LH_query_data(self):
        for i in range(self.query_retry):
            try:
                with request.urlopen(self.url, timeout=self.timeout) as response:
                    result = response.read().decode('cp949')
                    dictionary = xmltodict.parse(result)        # JSON ?????? ??????
                    json_object = json.dumps(dictionary)
                    self.json_data = json.loads(json_object)

                    return True
            except Exception as e:
                self.logger.error(e)
        return False

# ETRI_API
    # ?????? ????????????
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

    # ???????????? ????????????
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

    # ????????????, ??????, ?????? ????????? ?????? ????????????
    def get_ETRI_query_data(self, page, headerr, type):
        temp_arr = []
        # 3:???????????? 4:???????????? 5:???????????? 6:????????????
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
            check = '??????'  # ?????? ?????? ???

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

                    if(tables[0][0][1] == '????????? ???????????? ????????????.'):
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
                        # ?????? (ex. [????????????(??????), ???????????????, ???????????????, ????????????])
                        self.result_arr.append([[tables[0][1][j], tables[0][4][j], tables[0][5][j], tables[0][7][j]] for j in range(1, len(tables[0][0]))])
                        self.page_check += 1
                    else:
                        # ?????? (ex. [????????????(??????), ???????????????, ???????????????, ????????????])
                        self.result_arr.append([[tables[0][0][j], tables[0][3][j], tables[0][4][j], tables[0][6][j]] for j in range(1, len(tables[0][0]))])
                        self.page_check += 1

                    # ??????????????? ????????? ??????
                    if  self.page_check > 2:
                        if self.check_change_list(self.page_check) is False:
                            return 'back'
                    return True
            except Exception as e:
                self.logger.error(e)
        return False

    # ????????? ?????????
    def get_ETRI_items(self, type):
        try:
            self.item_data = []
            for bidnum_degree in self.bidnum_degree:
                url = f'{self.url}?biNo={bidnum_degree[0]}'     # URL ??????
                print(url)
                if type == 3:   # ????????????
                    item = self.get_ETRI_announce(url)
                    item.update(self.get_ETRI_ex_info(ETRI_web.ex_info_URL,bidnum_degree[0]))   # ?????? ??? ????????? ????????????
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
                elif type == 4:  # ????????????
                    item = self.get_ETRI_result(url)
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
                elif type == 5:  # ????????????
                    item = self.get_ETRI_announce(url)
                    item.update(self.get_ETRI_ex_info(ETRI_web.ex_info_URL,bidnum_degree[0]))   # ?????? ??? ????????? ????????????
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
                elif type == 6:  # ????????????
                    item = self.get_ETRI_result(url)
                    self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
            return True
        except KeyError as e:
            self.logger.error(e)
        return False

    # ????????????
    def exfile_cw(self, count):
        temp_arr = []
        # url ????????????
        url_arr = [self.get_etri_file(file) for file in self.table[-1].find_all('a')]
        for i in range(1, len(self.tables[count].index)):
            item_dic = {}
            for j in range(0, len(self.tables[count].columns)):
                item_dic[self.tables[count][j][0]] = self.tables[count][j][i]
            item_dic['URL'] = url_arr[i-1]
            temp_arr.append(item_dic)

        return temp_arr

    # ????????? ??????, ??????, ?????????, ????????? 
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
        # ?????? ????????????
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
            #nan??????
            for i in range(0, len(self.tables)):
                self.tables[i] = self.tables[i].fillna('')

            t_len = len(self.tables[0])

            # ????????????
            for i in range(0, len(self.tables[0][0]) - 2):
                result_dic[self.strip_re(self.tables[0][0][i])] = self.strip_re(self.tables[0][1][i])
                result_dic[self.strip_re(self.tables[0][3][i])] = self.strip_re(self.tables[0][4][i])

            item_dic[self.strip_re(self.tables[0][1][t_len-2])] = [self.strip_re(self.tables[0][2][t_len-2]), self.strip_re(self.tables[0][3][t_len-2]), self.strip_re(self.tables[0][4][t_len-2])]
            item_dic[self.strip_re(self.tables[0][1][t_len-1])] = [self.strip_re(self.tables[0][2][t_len-1]), self.strip_re(self.tables[0][3][t_len-1]), self.strip_re(self.tables[0][4][t_len-1])]
            result_dic[self.strip_re(self.tables[0][0][t_len-1])] = item_dic

            # ????????????
            result_dic['????????????'] = self.columns_cw(1)

            # ??????????????????
            result_dic[self.strip_re(self.tables[2][0][0])] = self.strip_re(self.tables[2][1][0])

            # ????????????
            result_dic['????????????'] = self.liner_cw(3, 0, 2, 0)
        
            if (len(self.tables)) > 5:
                # ???????????? ????????????
                result_dic['????????????????????????'] = self.liner_cw(4, 0, 2, 0)
                # ????????????
                result_dic['????????????????????????'] = self.exfile_cw(5)
            elif(len(self.tables)) <= 5:
                # ????????????
                result_dic['????????????????????????'] = self.exfile_cw(4)

            return result_dic

    def get_ETRI_result(self, url):
        result_dic = {}
        # ?????? ????????????
        for i in range(self.query_retry):
            if self.get_ETRI_cookie() is False:
                sleep(self.timeout)
                continue

            # ?????? ????????????
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

            #nan??????
            for i in range(0, len(self.tables)):
                self.tables[i] = self.tables[i].fillna('')

            # ????????????
            result_dic['????????????'] = self.liner_cw(1, 0, 2, 0)
            if(len(self.tables) > 2):
                # ?????? ???????????? ??? ????????????
                if(len(self.tables) == 3):
                    # ????????????
                    result_dic['????????????'] = self.columns_cw(2)
                else:
                    result_dic['??????????????????'] = self.liner_cw(2, 0, 3, 1)

                    result_dic['???????????? ??? ????????????'] = self.liner_cw(2, 3, 1, 1)

                    # ????????????
                    result_dic['????????????'] = self.columns_cw(3)

            return result_dic


    # ?????? ??? (???????????? ????????????)
    def get_ETRI_ex_info(self, url, bidnum_degree):

        for i in range(self.query_retry):
            # ?????? ????????????
            if self.get_ETRI_cookie() is False:
                sleep(self.timeout)
                continue                

            url = url + f'?biNo={bidnum_degree}'    # URL??? ?????? ?????? ??????
            # ?????? ????????????
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
                    if(i == en.????????????):     # ????????????
                        result_dic['????????????'] = []
                        # key??? ????????????
                        for body in value.find_all('td', class_='list01'):
                            if(self.strip_re_w(body) == '????????????'):    # ?????? ???????????? ??????
                                temp_arr.append(self.strip_re_w(body))
                                break
                            temp_arr.append(self.strip_re_w(body))
                        # value ??? ????????????
                        for body in value.find_all('td', class_=''):
                            if(j == len(temp_arr)-1):
                                item_dic[temp_arr[j]] = self.strip_re_w(body)
                                j = 0
                                item_arr.append(item_dic)
                                result_dic['????????????'].append(item_arr)
                                item_dic = {}
                                item_arr = []
                            else:
                                item_dic[temp_arr[j]] = self.strip_re_w(body)
                                j += 1
                    i += 1
            else:
                return False
            return result_dic
