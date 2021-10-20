class Schema():
    def get_table_list(self):
        return [
            '''
            CREATE TABLE IF NOT EXISTS "public"."raw_lh_announce" (
                "seq" BIGSERIAL,
                "begin_dt" CHAR(12) NOT NULL,
                "end_dt" CHAR(12) NOT NULL,
                "text" JSON NOT NULL,
                "process" SMALLINT DEFAULT 0 NOT NULL,
                "reg_dt" TIMESTAMP DEFAULT now() NOT NULL,
                PRIMARY KEY("seq")
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS "public"."raw_lh_result" (
                "seq" BIGSERIAL,
                "begin_dt" CHAR(12) NOT NULL,
                "end_dt" CHAR(12) NOT NULL,
                "text" JSON NOT NULL,
                "process" SMALLINT DEFAULT 0 NOT NULL,
                "reg_dt" TIMESTAMP DEFAULT now() NOT NULL,
                PRIMARY KEY("seq")
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS "public"."raw_etri_result" (
                "seq" BIGSERIAL,
                "begin_dt" CHAR(12) NOT NULL,
                "end_dt" CHAR(12) NOT NULL,
                "text" JSON NOT NULL,
                "process" SMALLINT DEFAULT 0 NOT NULL,
                "reg_dt" TIMESTAMP DEFAULT now() NOT NULL,
                PRIMARY KEY("seq")
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS "public"."raw_etri_announce" (
                "seq" BIGSERIAL,
                "begin_dt" CHAR(12) NOT NULL,
                "end_dt" CHAR(12) NOT NULL,
                "text" JSON NOT NULL,
                "process" SMALLINT DEFAULT 0 NOT NULL,
                "reg_dt" TIMESTAMP DEFAULT now() NOT NULL,
                PRIMARY KEY("seq")
            )
            '''
        ]
    def get_index_list(self):
        return [
            'CREATE INDEX ON "raw_lh_announce"("process") WHERE "process" = 0',
            'CREATE INDEX ON "raw_lh_announce"("reg_dt")',
            'CREATE INDEX ON "raw_lh_result"("process") WHERE "process" = 0',
            'CREATE INDEX ON "raw_lh_result"("reg_dt")',
            'CREATE INDEX ON "raw_etri_result"("process") WHERE "process" = 0',
            'CREATE INDEX ON "raw_etri_result"("reg_dt")',
            'CREATE INDEX ON "raw_etri_announce"("process") WHERE "process" = 0',
            'CREATE INDEX ON "raw_etri_announce"("reg_dt")'
        ]

if __name__ == '__main__':
    import psycopg2
    import psycopg2.extras

    from config import DBConfig

    schema = Schema()

    connection = psycopg2.connect(host=DBConfig.host, dbname=DBConfig.dbname, user=DBConfig.user, password=DBConfig.password, port=DBConfig.port)
    cursor = connection.cursor()
    connection.set_session(autocommit=True)

    tables = schema.get_table_list()
    for t in tables:
        cursor.execute(t)

    indexes = schema.get_index_list()
    for i in indexes:
        cursor.execute(i)

    cursor.close()
    connection.close()
