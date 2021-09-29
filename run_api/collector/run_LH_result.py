import time

from requests import api
from lib.config import LH_Api
from lib.state import StateCode
from api import G2B
from data import G2BData

#DB
from lib.db import Db
from lib.logger import Logger

class LHResultRunner():
    rows = 10
    sleep_time = 1

    def __init__(self, key, begin, end):
        self.logger = Logger.get_logger('collector')
        LH_key = LH_Api.key
        self.key = LH_key
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
            bid_list.append(g2b_data.get_LH_result())
            
            #bid_list = [[url, div, filtering, table] for url, divs, table in bid_list for div, filtering in divs.items()]

            for url,table in bid_list:
                if self.url(url, table) is False:
                    state_code = StateCode.ERROR
                    self.db.rollback()
                    return False
                else:
                    self.db.commit()
        except Exception as e:
            print("ERROR g2b")
        finally:
            print("FIN")
            self.db.close()
            #State.update_state(self.logger, __class__, __file__, state_code, self.begin, self.end)

    def url(self, url, table):
        print('url start')
        print(self.begin, self.end)
        g2b = G2B( self.begin, self.end)

        page = 1
        while True:
            query = f'serviceKey={self.key}&numOfRows={self.rows}&pageNo={page}&openDtmStart={self.begin}&openDtmEnd={self.end}'
            g2b.set_query_url(f'{url}?{query}')
            g2b.set_page(page, self.rows)
            if g2b.query_data(2) is False:
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
