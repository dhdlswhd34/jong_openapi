import time

from lib.state import StateCode
from api import G2B
from data import G2BData

from lib.logger import Logger
# DB
from lib.db import Db


class ETRICustRunner():
    rows = 10
    sleep_time = 1

    def __init__(self, key, begin, end):
        self.logger = Logger.get_logger('collector')
        self.begin = begin
        self.end = end

    def exec(self):
        # DB부분
        self.db = Db(self.logger)
        self.db.connect()
        self.db.autocommit(False)

        try:
            g2b_data = G2BData()
            bid_list = []
            bid_list.append(g2b_data.get_ETRI_cust())   # URL, DB테이블 받아오기

            for url, table in bid_list:
                if self.url(url, table) is False:    # URL 접근
                    # state_code = StateCode.ERROR
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

        g2b = G2B(self.begin, self.end)  #API 가져오기

        if g2b.get_ETRI_cookie() is False:
            return False
        self.header = {'Cookie': g2b.cookie}    # 접근시 쿠키 필요(ETRI)

        page = 1
        while True:
            # 3:입찰공고 4:개찰결과 5:견적문의 6:견적결과
            if g2b.get_ETRI_query_data(page, self.header, 5) == 'end':  # 결과 목록 리스트 공고번호 가져오기
                break
            page += 1

        # 1:입찰공고 2:개찰결과 3:견적문의 4:견적결과
        g2b.check_ETRI_query_data(3)    # 새로운 리스트 유무 탐색

        g2b.set_query_url(f'{url}')     # 데이터 크롤링을 위한 url

        # 3:입찰공고 4:개찰결과 5:견적문의 6:견적결과
        if g2b.get_ETRI_items(5) is False:  # 개찰 결과 크롤링
            return False

        if self.item_insert(table, g2b.item_data) is False:     # DB에 넣기
            return False

    def item_insert(self, table, sql_data):
        if sql_data:
            sql = f'insert into {table}(begin_dt, end_dt, text) values(%s, %s, %s)'
            if self.db.bulk_execute(sql, sql_data) is False:
                return False
            else:
                self.logger.debug(f'table({table}), insert count({len(sql_data)})')
