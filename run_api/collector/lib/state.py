from datetime import datetime
from enum import Enum
import os



class StateCode(Enum):
    PROCEEDING = '1'
    END = '2'
    ERROR = '3'
"""
class State():
    process_pid = None

    @classmethod
    def update_state(cls, logger, call, file, state, begin=None, end=None):
        db = Db(logger)
        db.connect()

        try:
            parent = os.path.basename(os.path.dirname(file))
            name = call.__name__
            column = 'end_dt' if state == StateCode.END else 'start_dt'

            if state == StateCode.PROCEEDING or cls.process_pid is None:
                pid = os.getpid()
                epoch = int(datetime.now().timestamp())
                cls.process_pid = f'{pid}{epoch}'

            sql = 'select state from process where parent = %s and name = %s'
            sql_data = (parent, name)
            if db.query(sql, sql_data, 'one') is True and db.rows:
                if state.value == db.rows['state']:
                    logger.error(f'process state error({state.value})')
                    return False

                if state == StateCode.END:
                    sql = 'update process set state = %s, collect_end = %s where parent = %s and name = %s returning seq'
                    sql_data = (state.value, end, parent, name)
                else:
                    sql = 'update process set state = %s where parent = %s and name = %s returning seq'
                    sql_data = (state.value, parent, name)
            else:
                sql = 'insert into process(parent, name, state) values(%s, %s, %s) returning seq'
                sql_data = (parent, name, state.value)

            if db.execute(sql, sql_data) is False:
                return False

            process_seq = db.last_id()

            sql = 'select seq from process_log where ref_seq = %s and pid = %s'
            sql_data = (process_seq, cls.process_pid)
            if db.exists(sql, sql_data) is False:
                sql = f'insert into process_log(ref_seq, pid, collect_begin, collect_end, {column}) values(%s, %s, %s, %s, localtimestamp)'
                sql_data = (process_seq, cls.process_pid, begin, end)
            else:
                sql = f'update process_log set {column} = localtimestamp where ref_seq = %s and pid = %s'
                sql_data = (process_seq, cls.process_pid)

            if db.execute(sql, sql_data) is False:
                return False
        finally:
            db.close()

"""