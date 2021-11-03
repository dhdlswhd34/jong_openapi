import time

from lib.state import StateCode
from api import G2B
from data import G2BData

from lib.logger import Logger
# DB
from lib.db import Db


class ETRIResultRunner():
    rows = 10
    sleep_time = 1

    def __init__(self, key, begin, end):
        self.logger = Logger.get_logger('collector')
        self.begin = begin
        self.end = end

    def exec(self):
        state_code = StateCode.PROCEEDING

        #DB부분
        self.db = Db(self.logger)
        self.db.connect()
        self.db.autocommit(False)

        try:
            g2b_data = G2BData()
            bid_list = []
            bid_list.append(g2b_data.get_ETRI_result()) # URL, DB테이블 받아오기

            for url, table in bid_list:
                if self.url(url, table) is False:   # URL 접근
                    self.db.rollback()
                    return False
                else:
                    self.db.commit()
        except Exception as e:
            self.logger.error(e)
        finally:
            print("FIN")
            self.db.close()

    def url(self, url, table):
        print('url start')

        g2b = G2B(self.begin, self.end)     #API 가져오기

        if g2b.get_ETRI_cookie() is False:
            return False
        self.header = {'Cookie': g2b.cookie}    # 접근시 쿠키 필요(ETRI)

        page = 1
        while True:
            # 3:입찰공고 4:개찰결과 5:견적문의 6:견적결과
            state = g2b.get_ETRI_query_data(page, self.header, 4)
            if state == 'end':  # 결과 목록 리스트 공고번호 가져오기
                break
            elif state == 'back':
                page = 0
                g2b.result_arr.clear()
            page += 1

        if self.check_ETRI_query_data_db(g2b.result_arr, g2b.bidnum_degree) is False:
            return False

        g2b.set_query_url(f'{url}')     # 데이터 크롤링을 위한 url
        
        # 3:입찰공고 4:개찰결과 5:견적문의 6:견적결과
        if g2b.get_ETRI_items(4) is False:  # 개찰 결과 크롤링
            return False

        if self.item_insert(table, g2b.item_data, 'data') is False: # DB에 넣기
            return False

    def check_ETRI_query_data_db(self,result_arr ,bidnum_degree):
        temp_list = []

        table = 'raw_etri_result_list'

        # 마지막 데이터 불러오기
        query = f'SELECT bidnum, start_dt, end_dt, process FROM {table}'
        self.db.cursor.execute(query)

        db_list = self.db.cursor.fetchall()

        if len(db_list) > 1:
            # 추가 내용 저장
            for pg in result_arr:
                for bidnum, start_dt, end_dt, process in pg:
                    i = 1
                    for temp_db in db_list:
                        if (bidnum == temp_db[0].strip() and # 공고번호 차수
                            start_dt == temp_db[1].strip() and # 입찰시작일
                            end_dt == temp_db[2].strip() and # 입찰종료일
                            process == temp_db[3].strip()):   # 진행상태
                            i = 0          
                    if(i == 1):     # 새로운 데이터 저장
                        #저장 (ex. 공고번호(차수),입찰시작일,입찰종료일,진행상태)
                        temp_list.append((bidnum, start_dt, end_dt, process))
                        bidnum_degree.append([bidnum, process])   # 새로운 리스트 공고번호 저장
        else:
            for pg in result_arr:
                for bidnum, start_dt, end_dt , process in pg:
                    temp_list.append((bidnum, start_dt, end_dt, process))
                    bidnum_degree.append([bidnum, process])   # 새로운 리스트 공고번호 저장

        if self.item_insert(table, temp_list, 'list') is False: # DB에 넣기
            return False
        
        return True

    def item_insert(self, table, sql_data, type):
        if sql_data:
            if(type == 'data'):
                sql = f'insert into {table}(begin_dt, end_dt, text) values(%s, %s, %s)'
            if(type == 'list'):
                sql = f'insert into {table}(bidnum, start_dt, end_dt, process) values(%s, %s, %s, %s)'
            if self.db.bulk_execute(sql, sql_data) is False:
                return False
            else:
                self.logger.debug(f'table({table}), insert count({len(sql_data)})')
