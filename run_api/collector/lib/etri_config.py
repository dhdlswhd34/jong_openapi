class ETRI_web:
    URL = 'https://ebid.etri.re.kr/ebid/index.do'
    D_URL = 'https://ebid.etri.re.kr/ebid/download.do'
    check_URL = 'https://ebid.etri.re.kr/ebid/ebid/ebidCustProgressList.do'
    cust_URL = 'https://ebid.etri.re.kr/ebid/ebid/ebidEstmtRqstList.do'
    ex_info_URL = 'https://ebid.etri.re.kr/ebid/ebid/ebidCustInfoExAmtView.do'


class announce_enum():
    공고번호정보 = 0
    입찰일정 = 1
    입찰참고사항 = 2
    가격정보 = 3
    적격심사세부기준 = 4
    입찰공고안내서류 = 5


class result_enum():
    최종결과 = 1
    복수예비가격 = 2
    개찰결과 = 3


class ex_enum():
    물품내역 = 1
