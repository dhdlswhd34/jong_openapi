from datetime import datetime
from urllib import request
import json
import time
import xmltodict

# 나중에 정리
from bs4 import BeautifulSoup
import requests
from lib.lh_config import LH_web, label_list
from urllib.parse import quote_plus


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

    def get_ETRI_webc(self, url):
        temp_dict = {}
        response = requests.get(self.url)

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

    def get_LH_items(self, type):
        try:
            self.r_item = self.json_data["response"]["body"]["item"]

            self.item_data = []

            if self.filtering is None:
                for item in self.r_item:

                    self.bidNum = item.get('bidNum')
                    self.bidDegree = item.get('bidDegree')

                    if type == 1:
                        item['입찰공고'] = self.get_LH_dict(LH_web.URL)
                        item['입찰공고'].update(self.get_LH_dict_file())
                        self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))
                    elif type == 2:
                        self.item_data.append((self.begin, self.end, json.dumps(item, ensure_ascii=False)))             
            return True
        except KeyError as e:
            self.logger.error(e)
            return False

    def query_page(self):
        self.get_total_count()
        (q, r) = divmod(self.total_count, self.rows)
        self.page_count = q if r == 0 else q + 1

    def query_data(self, type, retry=0):

        if self.get_LH_query_data() is False:
            return False

        self.get_result_code()

        if self.result_code == 0:
            if self.page == 1:
                self.query_page()

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
