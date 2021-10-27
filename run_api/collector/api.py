from datetime import datetime
from urllib import request
import json
import time
import xmltodict
import requests
from bs4 import BeautifulSoup
from lib.lh_config import LH_web, label_list
from lib.etri_config import ETRI_web, p_list 
from urllib.parse import quote_plus
from functools import reduce
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
        self.result_arr = []

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
            print(response.status_code)
            return False

    # 첨부파일 가져오기
    def get_etri_file(self, body):
        temp = re.search('\'.+\'', body['onclick']).group()[1:]
        temp = reduce(lambda src, filter: src.replace(filter, ''), ['\'', ' '], temp)
        temp = temp.split(',')
        url = f'{ETRI_web.D_URL}?file_id={temp[0]}&file_gb={temp[1]}'
        return url

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
            check = '견적완료'  # 견적완료는 따로 check

        k = 0
        for i in range(self.query_retry):
            try:
                with requests.get(url, headers=self.header) as response_result:
                    if response_result.status_code == 200:
                        html = response_result.text
                        soup_obj = BeautifulSoup(html, 'html.parser')
                    else:
                        return False
                    for value in soup_obj.find('table', id='table01').find_all('tr'):
                        for body in value.find_all('td'):
                            if body.text.strip() == '자료가 존재하지 않습니다.':   # 마지막 페이지
                                k = -1
                                break
                            # 공고번호 차수
                            temp = re.search(f'E[A-Z]{self.begin[0:4]}.+\)', body.text.strip())      # ex) EA20210000(01) EP~ ,EE~
                            # 시작일시 , 종료일시 
                            temp_S = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', body.text.strip())   #ex) 2021-00-00 00:00 (년-월-일 시:분) 
                            if temp is not None:
                                temp_arr.append(temp.group())
                            if temp_S is not None:
                                temp_arr.append(temp_S.group())
                            # 진행 상태 (ex. 진행, 개찰, 유찰 등등)
                            for match in p_list:
                                if match == self.strip_re(body):
                                    if(type == 6 and check != match):   # 견적결과는 따로 체크 후 저장
                                        temp_arr = []
                                        break
                                    temp_arr.append(self.strip_re(body))
                                    break
                        if len(temp_arr) > 1:
                            self.result_arr.append(temp_arr)    # 저장 (ex. [공고번호(차수), 입찰시작일, 입찰종료일, 진행상태])
                        temp_arr = []
                    if(k == -1):
                        print(url)
                        return 'end'    # 마지막 페이지
                    return True
            except Exception as e:
                self.logger.error(e)
        return False

    # 파일 체크
    def check_ETRI_query_data(self, type):
        self.bidunm_degree = []

        # 1:입찰공고 2:개찰결과 3:견적문의 4:견적결과
        list_arr = []
        if(type == 1):
            txt = 'etri_announce.txt'
        elif(type == 2):
            txt = 'etri_result.txt'
        elif(type == 3):
            txt = 'etri_cust.txt'
        elif(type == 4):
            txt = 'etri_cust_result.txt'

        # 마지막 데이터 불러오기
        f = open(f'{txt}', 'rt', encoding='UTF8')
        while True:
            line = f.readline()
            if not line:
                break
            line = line.split(',')
            list_arr.append(line)
        f.close()

        # 추가 내용 저장
        f = open(f'{txt}', 'a+', encoding='UTF8')
        for bs in self.result_arr:
            i = 1
            for txt in list_arr:
                if(txt[0:4] == bs):     # 중복체크
                    i = 0   # 중복인 경우 0
                    break   # 발견시 break
            if(i == 1):     # 새로운 데이터 저장
                current_time = datetime.now()
                f.write(f'{bs[0]},{bs[1]},{bs[2]},{bs[3]},{current_time}\n')    #저장 (ex. 공고번호(차수),입찰시작일,입찰종료일,진행상태,현재시각 )
                self.bidunm_degree.append([bs[0], bs[3]])   # 새로운 리스트 공고번호 저장
        f.close()

    # 데이터 크롤링
    def get_ETRI_items(self, type):
        try:
            self.item_data = []
            for bidnum_degree in self.bidunm_degree:
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

    # 입찰공고 데이터
    def get_ETRI_announce(self, url):
        # 쿠키 가져오기
        if self.get_ETRI_cookie() is False:
            return False

        response = requests.get(url, headers=self.header)

        if response.status_code == 200:
            html = response.text
            self.soup_obj = BeautifulSoup(html, 'html.parser')
        else:
            print(response.status_code)

        if (self.soup_obj.find_all('table', id='table01')) is not None:
            i = 0
            result_dic = {}
            for value in self.soup_obj.find_all('table', id='table01'):
                j = 0
                temp_arr = []
                item_arr = []
                item_dic = {}
                if (i == 0):    # 공고번호 정보
                    item_arr = []
                    # key값 가져오기
                    for body in value.find_all('td', class_='name02'):
                        item_arr.append(self.strip_re(body))
                    # value값 가져오기
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
                    result_dic['입찰일정'] = []
                    # key값 가져오기
                    for body in value.find_all('td', class_='list01'):
                        temp_arr.append(self.strip_re(body))
                    # value값 가져오기
                    for body in value.find_all('td', class_=''):
                        if(j == len(temp_arr) - 1):
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
                    result_dic['가격정보(단위:원)'] = {}
                    # key값 가져오기
                    for body in value.find_all('td', class_='name02'):
                        temp_arr.append(self.strip_re(body))
                    # value값 가져오기
                    for body in value.find_all('td', class_=''):
                        if(j == (len(temp_arr) - 1)):
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            result_dic['가격정보(단위:원)'] = item_dic
                        else:
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            j += 1
                if(i >= 4) and len(value.find_all('td', class_='name02')) > 1:     # 적격심사 세부기준
                    result_dic['적격심사 세부기준'] = []
                    # key값 가져오기
                    for body in value.find_all('td', class_='name02'):
                        temp_arr.append(self.strip_re(body))
                    # value값 가져오기
                    for body in value.find_all('td', class_=''):
                        if(j == (len(temp_arr) - 1)):
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            j = 0
                            item_arr.append(item_dic)
                            result_dic['적격심사 세부기준'].append(item_arr)
                            item_dic = {}
                            item_arr = []
                        else:
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            j += 1
                if(i >= 4) and (value.find_all('td', class_='list01')) is not None:     # 입찰공고안내서류
                    result_dic['입찰공고안내서류'] = []
                    # key값 가져오기
                    for body in value.find_all('td', class_='list01'):
                        temp_arr.append(self.strip_re(body))
                    # value값 가져오기
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
        # 쿠키 가져오기
        if self.get_ETRI_cookie() is False:
            return False

        # 쿠키 넣어주기
        response = requests.get(url, headers=self.header)

        if response.status_code == 200:
            html = response.text
            self.soup_obj = BeautifulSoup(html, 'html.parser')
        else:
            print(response.status_code)

        if (self.soup_obj.find('table', id='table01')) is not None:
            i = 0
            result_dic = {}
            for value in self.soup_obj.find_all('table', id='table01'):
                j = 0
                temp_arr = []
                item_arr = []
                item_dic = {}
                if (i == 1):    # 최종결과
                    for body in value.find_all('td'):
                        # key값 가져오기
                        if j == 0:
                            temp = self.strip_re(body)
                            j = 1
                        # value값 가져오기
                        else:
                            result_dic[temp] = self.strip_re(body)
                            j = 0
                if (i == 2):    # 복수 예비가격 및 예정가격
                    for body in value.find_all('tr'):
                        # key값 가져오기
                        if body.find('td', class_='name02') is None:
                            i += 1
                            break
                        # value값 가져오기
                        if j == 0:
                            for item in body.find_all('td'):
                                result_dic[item.text.strip()] = []
                            j = 1
                        elif j == 1:
                            for item in body.find_all('td')[0:-1]:
                                result_dic['복수예비가격'].append(item.text.strip())
                            item_arr.append(body.find_all('td', class_='list01')[0].text.strip())
                            item_arr.append(body.find_all('td', class_='list01')[-1].text.strip())
                            result_dic['추첨결과 및 예정가격'].append(item_arr)
                            item_arr = []
                if (i == 3):    # 개찰결과
                    result_dic['개찰결과'] = []
                    # key값 가져오기
                    for body in value.find_all('td', class_='list01'):
                        temp_arr.append(self.strip_re(body))
                    # value값 가져오기
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

    # 추가 탭 (입찰내역 가져오기)
    def get_ETRI_ex_info(self, url, bidnum_degree):
        # 쿠키 가져오기
        if self.get_ETRI_cookie() is False:
            return False

        url = url + f'?biNo={bidnum_degree}'    # URL이 달라 따로 설정
        # 쿠키 넣어주기
        response = requests.get(url, headers=self.header)

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
                temp_arr = []
                item_arr = []
                item_dic = {}
                if(i == 1):     # 물품내역
                    result_dic['물품내역'] = []
                    # key값 가져오기
                    for body in value.find_all('td', class_='list01'):
                        if(self.strip_re(body) == '물품명세'):    # 물품 명세에서 끊기
                            temp_arr.append(self.strip_re(body))
                            break
                        temp_arr.append(self.strip_re(body))
                    # value 값 가져오기
                    for body in value.find_all('td', class_=''):
                        if(j == len(temp_arr)-1):
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            j = 0
                            item_arr.append(item_dic)
                            result_dic['물품내역'].append(item_arr)
                            item_dic = {}
                            item_arr = []
                        else:
                            item_dic[temp_arr[j]] = self.strip_re(body)
                            j += 1
                i += 1
        else:
            return False
        return result_dic
