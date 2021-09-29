from datetime import datetime
from urllib import request
import json
import time
import xmltodict

#나중에 정리
from bs4 import BeautifulSoup
import requests
from lib.config import LH_web ,LH_web_result
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

    """
    def get_query_data(self):
        for i in range(self.query_retry):
            try:
                with request.urlopen(self.url, timeout=self.timeout) as response:
                    result = response.read().decode('UTF-8')
                    self.json_data = json.loads(result)
                    return True
            except Exception as e:
                self.logger.error(e)
                if 'result' in locals():
                    self.logger.error(result)
                time.sleep(self.query_retry_time)

        return False
    """


    def get_LH_dict(self,url):
        temp_dict = {}

        url = url +self.bidNum +'&bidDegree=' + self.bidDegree
        response = requests.get(url)
        
        if response.status_code == 200:
            html = response.text
            self.soup_obj = BeautifulSoup(html, 'html.parser')
        else : 
            print(response.status_code)
        for i in range(1,7):
            id_label1 = 'LblockDetail' + str(i)
            if(self.soup_obj.find('div', id = id_label1)) is not None:
                for value in self.soup_obj.find('div', id = id_label1).find_all('tr'):
                    label = value.find('th').find('label').text.strip()
                    data = value.find('td').text.strip()
                    if (label) == "국내/국제":
                        temp_dict[label] = data
                    elif (label) == "최초공고등록일":
                        temp_dict[label] = data
                    elif (label) == "가격점수제외금액":
                        temp_dict[label] = data
                    elif (label) == "낙찰제외기준금액":
                        temp_dict[label] = data
                    elif (label) == "비고":
                        temp_dict[label] = data
                    elif (label) == "공고변경사유":
                        temp_dict[label] = data
                    elif (label) == "입찰방식":
                        temp_dict[label] = data
                    elif (label) == "낙찰자선정방법":
                        temp_dict[label] = data
                    elif (label) == "심사적용기준":
                        temp_dict[label] = data
                    elif (label) == "지문인식공고여부":
                        temp_dict[label] = data
                    elif (label) == "재입찰":
                        temp_dict[label] = data
                    elif (label) == "PQ심사실시여부":
                        temp_dict[label] = data
                    elif (label) == "PQ심사신청서접수기한":
                        temp_dict[label] = data
                    elif (label) == "용역유형":
                        temp_dict[label] = data
                    elif (label) == "품명":
                        temp_dict[label] = data
                    elif (label) == "공사종류":
                        temp_dict[label] = data
                    elif (label) == "업종유형":
                        temp_dict[label] = data
                    elif (label) == "공종별내역서":
                        temp_dict[label] = data
                    elif (label) == "공고변경정보":
                        temp_dict[label] = data
            else:
                break
        return temp_dict

    def get_LH_dict_file(self):
        temp_dict = {
            '첨부파일' :{'순번':['파일명','URL']} 
            }    
        temp_list = []
        i = 1
        for value in self.soup_obj.find('div', class_ = "LblockListTable").find_all('tr',class_='Lfirst'):
            temp_list.append(value.find('a',class_='attach').text.strip())
            temp_list.append(self.file_url_get(value.find('a',class_='attach')['href']))
            temp_dict['첨부파일'][str(i)] = temp_list.copy()
            i += 1
            temp_list.clear()    
        return  temp_dict

    def file_url_get(self,ex_file):
        filename = ''
        savename = ''
        str_f = ''
        flag = False
        i = 0
        for value in ex_file:
            if value == "'":
                if(flag):
                    if(i == 1):
                        savename = str_f[1:]
                    elif(i == 3):
                        filename = str_f[1:]
                    i += 1
                    str_f = ''
                flag = not flag 
            if(flag):
                str_f += value

        savename = quote_plus(savename)
        filename = quote_plus(filename)

        file_url = 'https://ebid.lh.or.kr/ebid.framework.download.dev?download.filespec=bidinfo&download.filename=' + filename + '&download.savedname=' + savename + '&download.bidnum='
        
        return file_url




    #사용 X
    def get_LH_OTL_compay(self,url):
        temp_dict = {}
        temp_list = []

        url = url +self.bidNum +'&bidDegree=' + self.bidDegree
        response = requests.get(url)

        print(url)
        if response.status_code == 200:
            html = response.text
            self.soup_obj = BeautifulSoup(html, 'html.parser')
        else : 
            print(response.status_code)

        temp = ''
        if(self.soup_obj.find('div' ,class_ = 'Lwrapper')) is not None:
            for value in self.soup_obj.find('div' ,class_ = 'Lwrapper'):
                if(value.find('thead')) != -1:
                    for tag in value.find('thead').find_all('th'):
                        if tag.text.strip() != '순번':
                            temp_list.append(tag.text.strip())
                    temp_dict['순번'] = temp_list.copy()
                temp_list.clear()
                if(value.find('tbody')) != -1:
                    for tr in value.find('tbody').find_all('tr'):
                        for i in range(1,len(tr.find_all('td'))):
                            temp_list.append(tr.find_all('td')[i].text.strip())
                        temp_dict[tr.find('td').text] = temp_list.copy()
                        temp_list.clear()
        return temp_dict

    def get_LH_query_data(self):
        for i in range(self.query_retry):
            try:
                with request.urlopen(self.url, timeout=self.timeout) as response:
                    result = response.read().decode('cp949')
                    dictionary = xmltodict.parse(result) #JSON 으로 변환
                    json_object = json.dumps(dictionary)
                    self.json_data = json.loads(json_object)

                    """
                    self.r_item = self.json_data["response"]["body"]["item"]
                    #self.r_item = self.r_body.get("item")

                    j = 0
                    for item in self.r_item:
                        print(item.get('bidNum'))
                        self.bidNum = item.get('bidNum')
                        print(item.get('bidDegree'))
                        self.bidDegree = item.get('bidDegree')    
                        
                        if type == 1:
                            item['입찰공고'] = self.get_LH_dict(LH_web.URL)
                            item['입찰공고'].update(self.get_LH_dict_file())
                            with open('announce_json/'+str(item.get('bidNum'))+ '_' + str(item.get('bidDegree')) + '_announce.json', 'w', encoding='utf-8') as file :
                                json.dump(item, file, ensure_ascii=False, indent='\t')
                            #print(self.r_body)                        
                        elif type == 2:
                            with open('result_json/'+str(item.get('bidNum'))+ '_' + str(j) + '_result.json', 'w', encoding='utf-8') as file :
                                json.dump(item, file, ensure_ascii=False, indent='\t')
                            j+=1    
                    with open('announce_json/'+str(item.get('bidNum'))+ '_' + str(item.get('bidDegree')) + '_announce_total.json', 'w', encoding='utf-8') as file :
                        json.dump(self.r_item, file, ensure_ascii=False, indent='\t')     
                    """
                    return True
            except Exception as e:
                print('get_LH_query_data ERROR')    
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


    def get_LH_items(self,type):
        try:
            self.r_item = self.json_data["response"]["body"]["item"]

            self.item_data = []
            
            if self.filtering is None:
                for item in self.r_item:
                    print(str(type)+"|"+item.get('bidNum') + '|' +item.get('bidDegree'))
                    self.bidNum = item.get('bidNum')
                    self.bidDegree = item.get('bidDegree')    
    
                    if type == 1:
                        item['입찰공고'] = self.get_LH_dict(LH_web.URL)
                        item['입찰공고'].update(self.get_LH_dict_file())
                        self.item_data.append((self.begin, self.end,json.dumps(item,ensure_ascii=False)))
                    elif type == 2:
                        self.item_data.append((self.begin, self.end,json.dumps(item,ensure_ascii=False)))

            '''
            if self.filtering is None:
                self.item_data = [(self.begin, self.end, json.dumps(item, ensure_ascii=False)) for item in items]
                if self.sub_type == 'corporation':
                    self.sub_type_list = [item.get('bizno').strip() for item in items]
                elif self.sub_type == 'result':
                    self.sub_type_list = [(item.get('bidNtceNo'), item.get('bidNtceOrd'), item.get('bidClsfcNo'), item.get('rbidNo'), item.get('progrsDivCdNm')) for item in items]
                    self.sub_type_list = [tuple(map(str.strip, sub_type_item)) for sub_type_item in self.sub_type_list]
            elif isinstance(self.filtering, list):
                self.item_data = [(self.begin, self.end, json.dumps(item, ensure_ascii=False)) for item in items if self.list_calc_date(item)]
            else:
                self.item_data = [(self.begin, self.end, json.dumps(item, ensure_ascii=False)) for item in items if self.calc_date(item)]
                if self.sub_type == 'corporation':
                    self.sub_type_list = [item.get('bizno').strip() for item in items if self.calc_date(item)]
                elif self.sub_type == 'result':
                    self.sub_type_list = [(item.get('bidNtceNo'), item.get('bidNtceOrd'), item.get('bidClsfcNo'), item.get('rbidNo'), item.get('progrsDivCdNm')) for item in items if self.calc_date(item)]
                    self.sub_type_list = [tuple(map(str.strip, sub_type_item)) for sub_type_item in self.sub_type_list]
            '''    
            return True
        except KeyError as e:
            self.logger.error(e)
            return False


    def get_items(self):
        try:
            items = self.json_data['response']['body']['items']

            if self.filtering is None:
                self.item_data = [(self.begin, self.end, json.dumps(item, ensure_ascii=False)) for item in items]
                if self.sub_type == 'corporation':
                    self.sub_type_list = [item.get('bizno').strip() for item in items]
                elif self.sub_type == 'result':
                    self.sub_type_list = [(item.get('bidNtceNo'), item.get('bidNtceOrd'), item.get('bidClsfcNo'), item.get('rbidNo'), item.get('progrsDivCdNm')) for item in items]
                    self.sub_type_list = [tuple(map(str.strip, sub_type_item)) for sub_type_item in self.sub_type_list]
            elif isinstance(self.filtering, list):
                self.item_data = [(self.begin, self.end, json.dumps(item, ensure_ascii=False)) for item in items if self.list_calc_date(item)]
            else:
                self.item_data = [(self.begin, self.end, json.dumps(item, ensure_ascii=False)) for item in items if self.calc_date(item)]
                if self.sub_type == 'corporation':
                    self.sub_type_list = [item.get('bizno').strip() for item in items if self.calc_date(item)]
                elif self.sub_type == 'result':
                    self.sub_type_list = [(item.get('bidNtceNo'), item.get('bidNtceOrd'), item.get('bidClsfcNo'), item.get('rbidNo'), item.get('progrsDivCdNm')) for item in items if self.calc_date(item)]
                    self.sub_type_list = [tuple(map(str.strip, sub_type_item)) for sub_type_item in self.sub_type_list]

            return True
        except KeyError as e:
            self.logger.error(e)
            return False
    
    def query_page(self):
        self.get_total_count()
        (q, r) = divmod(self.total_count, self.rows)
        self.page_count = q if r == 0 else q + 1

    def query_data(self,type,retry=0):

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
