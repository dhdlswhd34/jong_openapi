class ETRI_web:
    URL = 'https://ebid.etri.re.kr/ebid/index.do'

    def file_url(savename, filename):
        return 'https://ebid.lh.or.kr/ebid.framework.download.dev?download.filespec=bidinfo&download.filename=' + filename + '&download.savedname=' + savename + '&download.bidnum='


label_list = [
    "국내/국제",
    "최초공고등록일",
    "가격점수제외금액",
    "낙찰제외기준금액",
    "비고",
    "공고변경사유",
    "입찰방식",
    "낙찰자선정방법",
    "심사적용기준",
    "지문인식공고여부",
    "재입찰",
    "PQ심사실시여부",
    "PQ심사신청서접수기한",
    "용역유형",
    "품명",
    "공사종류",
    "업종유형",
    "공종별내역서",
    "공고변경정보"
]
