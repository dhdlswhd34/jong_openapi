from lib.db import Db
from datetime import datetime, timedelta ,date


def change(db_list):
    for bs in [pg for pg in db_list]:
        bs[0] = 1


if __name__ == '__main__':
    db = Db()
    db.connect()
    db.autocommit(False)
    
    # today = date.today()
    # yesterday = date.today() - timedelta(1)
    # mon_ago = date.today() + timedelta(10)

    # print(today.strftime('%Y-%m-%d'))
    # print(yesterday.strftime('%Y-%m-%d'))
    # print(mon_ago.strftime('%Y-%m-%d'))

    table = 'raw_etri_announce_list'

    # query = f'DELETE FROM {table} where end_dt like \'{time}%\' '
    # db.cursor.execute(query)

    query = f'select bidnum,start_dt,end_dt,process FROM {table}'
    # # query = f'select end_dt FROM {table} order by end_dt ASC limit 1 '\
    

    db.cursor.execute(query)
    db_list = db.cursor.fetchall()

    # [print(t) for t in db_list]
    for bs in [pg for pg in db_list]:
        print(bs[0].strip())

    change(db_list)

    # for bs in [pg for pg in db_list]:
    #     print(bs)
    list = [[[1,2,3],[4,5,6],[7,8,9]],[[1,2,3],[14,15,16],[17,18,19]]]
    
    # for pg in list:
    #     for bs[0],bs[1],bs[2] in pg:
    #         print(bs[0] ,bs[1], bs[2])

    n_list = []
    
    for pg in list:
        for bs in pg:
            n_list.append(bs)

    print(n_list)
    print(tuple(set(n_list[0])))
    print(set([tuple(set(item)) for item in n_list]))

    # if (list[0] == 1 and # 1
    #     list[1] == 2 and # 1
    #     list[2] == 3 and # 1
    #     list[3] == 4 ):
    #     print("!!")
    


    # # print(db_list[0][0][0:10])
    # # year = db_list[0][0][0:4]
    # month = db_list[0][0][5:7]
    # day = db_list[0][0][8:10]
    # print(f'{year} {month} {day}')  
    

    # db.commit()
    # db.close()



