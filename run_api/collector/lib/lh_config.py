
class LH_Api:
    key = 'WImruyXsZ0iBn%2Bc1ZAB4oFgVpC8jU%2B%2Bspz4rAazLaglvajSPSWgPMxNQet72x79u6JUOqYp2SWlR5fhZPh6egQ%3D%3D'


class LH_web:
    URL = 'https://ebid.lh.or.kr/ebid.et.tp.cmd.BidsrvcsDetailListCmd.dev?bidNum='

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
