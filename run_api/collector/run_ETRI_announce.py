import time
from lib.state import StateCode
from api import G2B
from data import G2BData

from lib.logger import Logger
# DB
from lib.db import Db


class ETRIAnnounceRunner():
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
        # DB부분
        self.db = Db(self.logger)
        self.db.connect()
        self.db.autocommit(False)

        try:
            g2b_data = G2BData()
            bid_list = []
            bid_list.append(g2b_data.get_ETRI_announce())

            for url, table in bid_list:
                if self.url(url, table) is False:
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
            # State.update_state(self.logger, __class__, __file__, state_code, self.begin, self.end)

    def url(self, url, table):
        print('url start')

        g2b = G2B(self.begin, self.end)

        if g2b.get_ETRI_cookie() is False:
            return False
        self.header = {'Cookie': g2b.cookie}
    
        page = 1
        while True:
            # 공고번호 차수 가져오기
            if g2b.get_ETRI_query_data(page, self.header, 3) == 'end':
                break
            page += 1
            # time.sleep(self.sleep_time)

        # 1:입찰공고 2:개찰결과 3:견적문의
        g2b.check_ETRI_query_data(1)

        g2b.set_query_url(f'{url}')

        if g2b.get_ETRI_items(3) is False:
            return False

        if self.item_insert(table, g2b.item_data) is False:
            return False

    def item_insert(self, table, sql_data):
        if sql_data:
            sql = f'insert into {table}(begin_dt, end_dt, text) values(%s, %s, %s)'
            if self.db.bulk_execute(sql, sql_data) is False:
                return False
            else:
                self.logger.debug(f'table({table}), insert count({len(sql_data)})')
