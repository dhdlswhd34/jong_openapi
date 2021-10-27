from datetime import datetime


def del_old_line(type, time):

    # 1:입찰공고 2:개찰결과 3:견적문의 4:견적결과
    list_arr = []

    if(type == 1):
        txt = 'etri_announce.txt'
    elif(type == 2):
        txt = 'etri_result.txt'
    elif(type == 3):
        txt = 'etri_cust.txt'
    elif(type == 4):
        txt = 'etri_cust_result.txt'

    # 마지막 데이터 불러오기
    f = open(f'{txt}', 'rt', encoding='UTF8')
    while True:
        line = f.readline()
        if not line:
            break
        line = line.split(',')
        if line[2][0:10] != time:   # 현재 시작을 제외
            list_arr.append(line)
    f.close()

    # 저장
    with open(f'{txt}', 'w+t', encoding='UTF8') as f:
        for bs in list_arr:
            f.write(f'{bs[0]},{bs[1]},{bs[2]},{bs[3]},{bs[4]}\n')    # 저장 (ex. 공고번호(차수),입찰시작일,입찰종료일,진행상태,현재시각 )
        f.close()
