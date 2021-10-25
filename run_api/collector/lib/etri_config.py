
class ETRI_web:
    URL = 'https://ebid.etri.re.kr/ebid/index.do'
    D_URL = 'https://ebid.etri.re.kr/ebid/download.do'
    check_URL = 'https://ebid.etri.re.kr/ebid/ebid/ebidCustProgressList.do'
    cust_URL = 'https://ebid.etri.re.kr/ebid/ebid/ebidEstmtRqstList.do'
    ex_info_URL = 'https://ebid.etri.re.kr/ebid/ebid/ebidCustInfoExAmtView.do'

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