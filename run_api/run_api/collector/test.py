import psycopg2

test = None


try: # 다른 db 로 바꿀려면 재접속 해야함... 
    test  = psycopg2.connect(database="jong",user="jong",password="jong!",host="127.0.0.1",port="5432")
    cur = conn.cursor() # table 만들기 
    cur.execute("CREATE TABLE Cars(Id INTEGER PRIMARY KEY, Name VARCHAR(20), Price INT)") # data insert 
    cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)") 
    cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)") 
    cur.execute("SELECT * FROM Cars") 
    rows = cur.fetchall() 
    test.commit() 
except Exception as e: 
    print ('postgresql database connection error!')
    print (e)
    if test: 
        test.rollback() 
else: 
    print(rows)     
finally: 
    if test:
        test.close()
