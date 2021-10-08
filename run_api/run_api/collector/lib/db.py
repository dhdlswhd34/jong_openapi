import psycopg2
import psycopg2.extras

from lib.logger import Logger
from lib.config import DBConfig

class Db:
    connection = None
    query_logging = False

    def __init__(self, logger=None):
        self.logger = Logger.get_logger(__class__.__name__) if logger is None else logger

    def set_query_logging(self, query_logging):
        self.query_logging = query_logging

    def connect(self, cursor_factory=psycopg2.extras.DictCursor):
        self.connection = psycopg2.connect(host=DBConfig.host, dbname=DBConfig.dbname, user=DBConfig.user, password=DBConfig.password, port=DBConfig.port)
        self.cursor = self.connection.cursor(cursor_factory=cursor_factory)
        self.autocommit()

    def autocommit(self, mode=True):
        if self.connection:
            self.connection.set_session(autocommit=mode)

    def query(self, sql, data=None, opt='all'):
        try:
            if self.query_logging is True:
                self.logger.debug(f'sql->{sql}')

            if opt == 'one':
                return self.query_one(sql, data)
            elif opt == 'all':
                return self.query_all(sql, data)
            else:
                return False
        except Exception as e:
            self.logger.error(e, exc_info=True)
            self.logger.debug(f'sql->{sql}')
            self.logger.debug(f'data->{data}')
            return False

    def query_one(self, sql, data=None):
        if self.connection is None:
            return False

        if len(sql) == 0:
            return False

        try:
            if self.query_logging is True:
                self.logger.debug(f'sql->{sql}')

            self.cursor.execute(sql, data)
            self.rows = self.cursor.fetchone()
            return True
        except Exception as e:
            self.logger.error(e, exc_info=True)
            self.logger.debug(f'sql->{sql}')
            self.logger.debug(f'data->{data}')
            return False

    def query_all(self, sql, data=None):
        if self.connection is None:
            return False

        if len(sql) == 0:
            return False

        try:
            if self.query_logging is True:
                self.logger.debug(f'sql->{sql}')

            self.cursor.execute(sql, data)
            self.rows = self.cursor.fetchall()
            return True
        except Exception as e:
            self.logger.error(e, exc_info=True)
            self.logger.debug(f'sql->{sql}')
            self.logger.debug(f'data->{data}')
            return False

    def execute(self, sql, data=None):
        if self.connection is None:
            return False

        if len(sql) == 0:
            return False

        try:
            if self.query_logging is True:
                self.logger.debug(f'sql->{sql}')

            self.cursor.execute(sql, data)
            return True
        except Exception as e:
            self.logger.error(e, exc_info=True)
            self.logger.debug(f'sql->{sql}')
            self.logger.debug(f'data->{data}')
            return False

    def bulk_execute(self, sql, bulk):
        print("bulk_execute run")
        if self.connection is None:
            return False

        if len(sql) == 0:
            return False

        if not bulk:
            return False

        try:
            if self.query_logging is True:
                self.logger.debug(f'sql->{sql}')

            self.cursor.executemany(sql, bulk)
            print("executemany !")
            return True
        except Exception as e:
            self.logger.error(e, exc_info=True)
            self.logger.debug(f'sql->{sql}')
            return False

    def exists(self, sql, data=None):
        if self.connection is None:
            return False

        if len(sql) == 0:
            return False

        try:
            if self.query_logging is True:
                self.logger.debug(f'sql->{sql}')

            self.cursor.execute(sql, data)
            return self.cursor.fetchone() is not None
        except Exception as e:
            self.logger.error(e, exc_info=True)
            self.logger.debug(f'sql->{sql}')
            self.logger.debug(f'data->{data}')
            return False

    def last_id(self):
        if self.connection is None:
            return False

        try:
            return self.cursor.fetchone()[0]
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return None

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()

    def close(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()
