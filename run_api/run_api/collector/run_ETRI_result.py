import time

from requests import api
from lib.config import LH_Api
from lib.state import StateCode
from api import G2B
from data import G2BData

from lib.logger import Logger
#DB
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

        """
        if State.update_state(self.logger, __class__, __file__, state_code, self.begin, self.end) is False:
            return False
        else:
            state_code = StateCode.END

        """
        #DB부분
        self.db = Db(self.logger)
        self.db.connect()
        self.db.autocommit(False)

        try:
            g2b_data = G2BData()
            bid_list = []
            bid_list.append(g2b_data.get_ETRI_result())

            for url, table in bid_list:
                if self.url(url, table) is False:
                    # state_code = StateCode.ERROR
                    self.db.rollback()
                    return False
                else:
                    self.db.commit()
        except Exception as e:
            print("ERROR g2b")
        finally:
            print("FIN")
            self.db.close()
            # State.update_state(self.logger, __class__, __file__, state_code, self.begin, self.end)

    def url(self, url, table):
        print('url start')
        print(self.begin, self.end)
        g2b = G2B( self.begin, self.end)

        page = 1
        while True:
            query = f'biNo={self.bidnum}}%28{self.degree}%29&biBiz=C&biType=&biRound=1&vendorCode=&succDeciMeth=C&view=&actionCode=&biState=E&g2b_conn=&serverTime={self.year}%B3%E2+{self.month}%BF%F9+{self.date}%C0%CF+{self.hour}%BD%C3+{self.min}%BA%D0+{self.sec}%C3%CA&attend_yn=&tecdoc_submit_yn=&price_submit_yn=&tecdocSubmitStDate=&pageGb=C&etcMemoReadCheck=&sch_biNo=&sch_biName=&sch_succDeciMeth=&sch_biState=&sch_deptName=&sch_memberName=&sch_fromDate={self.start}&sch_toDate={self.end}&sch_biBizList=&sch_spotFromDate=&sch_spotToDate=&sch_enterFromDate=&sch_enterToDate=&search=Y&order=&pageNo=1&pageLine={page}'
            g2b.set_query_url(f'{url}?{query}')
            #g2b.set_page(page, self.rows)
            if g2b.get_ETRI_webc(2) is False:
                return False

            if page == 1:
                self.logger.debug(f'total count({g2b.total_count})')

                if g2b.total_count <= 0:
                    break

            self.logger.debug(f'page count({g2b.page_count}), page({page})')

            if self.item_insert(table, g2b.item_data) is False:
                return False

            break #체크포인트

            if g2b.page_count <= page:
                break

            page += 1

            time.sleep(self.sleep_time)


    def item_insert(self, table, sql_data):
        if sql_data:
            sql = f'insert into {table}(begin_dt, end_dt, text) values(%s, %s, %s)'
            if self.db.bulk_execute(sql, sql_data) is False:
                return False
            else:
                self.logger.debug(f'table({table}), insert count({len(sql_data)})')
