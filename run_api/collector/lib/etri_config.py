from enum import IntEnum

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


key_list = [
    'No',
    '사업자번호',
    '업체명',
    '대표자',
    '입찰금액',
    '투찰율',
    '추첨번호',
    '입찰일시',
    '비고'
    ]

p_list = [
    '진행',
    '개찰',
    '견적완료',
    '입찰완료',
    '완료(유찰)'
    ]
