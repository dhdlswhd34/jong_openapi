from datetime import datetime
from lib.db import Db

def del_db_old_line(type, time):
    db = Db()
    db.connect()
    db.autocommit(False)

    # 1:입찰공고 2:개찰결과 3:견적문의 4:견적결과
    if(type == 1):
        table = 'raw_etri_announce_list'
    elif(type == 2):
        table = 'raw_etri_result_list'
    elif(type == 3):
        table = 'raw_etri_cust_list'
    elif(type == 4):
        table = 'raw_etri_cust_result_list'

    # ex) delete from raw_etri_result_list where end_dt < '2021-10-28 24:00';
    query = f'DELETE FROM {table} WHERE end_dt < \'{time} 24:00\';'
    db.cursor.execute(query)

    db.commit()
    db.close()
