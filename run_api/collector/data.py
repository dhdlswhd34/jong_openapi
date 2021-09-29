class G2BData():
    def get_pre_standard_thing(self):
        url = 'http://apis.data.go.kr/1230000/HrcspSsstndrdInfoService/getPublicPrcureThngInfoThng'
        table = 'raw_pre_standard_thing'
        div = {'1': None, '3': 'rgstDt'}
        return [url, div, table]

    def get_pre_standard_thing_opinion(self):
        url = 'http://apis.data.go.kr/1230000/HrcspSsstndrdInfoService/getPublicPrcureThngOpinionInfoThng'
        table = 'raw_pre_standard_thing_opinion'
        div = {'1': None}
        return [url, div, table]

    def get_pre_standard_service(self):
        url = 'http://apis.data.go.kr/1230000/HrcspSsstndrdInfoService/getPublicPrcureThngInfoServc'
        table = 'raw_pre_standard_service'
        div = {'1': None, '3': 'rgstDt'}
        return [url, div, table]

    def get_pre_standard_service_opinion(self):
        url = 'http://apis.data.go.kr/1230000/HrcspSsstndrdInfoService/getPublicPrcureThngOpinionInfoServc'
        table = 'raw_pre_standard_service_opinion'
        div = {'1': None}
        return [url, div, table]

    def get_pre_standard_construction(self):
        url = 'http://apis.data.go.kr/1230000/HrcspSsstndrdInfoService/getPublicPrcureThngInfoCnstwk'
        table = 'raw_pre_standard_construction'
        div = {'1': None, '3': 'rgstDt'}
        return [url, div, table]

    def get_pre_standard_construction_opinion(self):
        url = 'http://apis.data.go.kr/1230000/HrcspSsstndrdInfoService/getPublicPrcureThngOpinionInfoCnstwk'
        table = 'raw_pre_standard_construction_opinion'
        div = {'1': None}
        return [url, div, table]

    def get_announce_thing(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoThng'
        table = 'raw_announce_thing'
        div = {'1': None, '3': 'rgstDt'}
        return [url, div, table]

    def get_announce_thing_basic_amount(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoThngBsisAmount'
        table = 'raw_announce_thing_basic_amount'
        div = {'1': None}
        return [url, div, table]

    def get_announce_thing_history(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoChgHstryThng'
        table = 'raw_announce_thing_history'
        div = {'1': None}
        return [url, div, table]

    def get_announce_thing_product(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoThngPurchsObjPrdct'
        table = 'raw_announce_thing_product'
        div = {'1': None}
        return [url, div, table]

    def get_announce_service(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoServc'
        table = 'raw_announce_service'
        div = {'1': None, '3': 'rgstDt'}
        return [url, div, table]

    def get_announce_service_basic_amount(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoServcBsisAmount'
        table = 'raw_announce_service_basic_amount'
        div = {'1': None}
        return [url, div, table]

    def get_announce_service_history(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoChgHstryServc'
        table = 'raw_announce_service_history'
        div = {'1': None}
        return [url, div, table]

    def get_announce_service_product(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoServcPurchsObjPrdct'
        table = 'raw_announce_service_product'
        div = {'1': None}
        return [url, div, table]

    def get_announce_construction(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoCnstwk'
        table = 'raw_announce_construction'
        div = {'1': None, '3': 'rgstDt'}
        return [url, div, table]

    def get_announce_construction_basic_amount(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoCnstwkBsisAmount'
        table = 'raw_announce_construction_basic_amount'
        div = {'1': None}
        return [url, div, table]

    def get_announce_construction_history(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoChgHstryCnstwk'
        table = 'raw_announce_construction_history'
        div = {'1': None}
        return [url, div, table]

    def get_announce_license(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoLicenseLimit'
        table = 'raw_announce_license'
        div = {'1': None}
        return [url, div, table]

    def get_announce_region(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoPrtcptPsblRgn'
        table = 'raw_announce_region'
        div = {'1': None}
        return [url, div, table]

    def get_announce_eorder(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListInfoEorderAtchFileInfo'
        table = 'raw_announce_eorder'
        div = {'1': None}
        return [url, div, table]

    def get_announce_innovation(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListPPIFnlRfpIssAtchFileInfo'
        table = 'raw_announce_innovation'
        div = {'2': None}
        return [url, div, table]

    def get_announce_cala(self):
        url = 'http://apis.data.go.kr/1230000/BidPublicInfoService02/getBidPblancListBidPrceCalclAInfo'
        table = 'raw_announce_cala'
        div = {'1': None}
        return [url, div, table]

    def get_open_result_thing(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoThng'
        table = 'raw_open_result_thing'
        div = {'1': None}
        return [url, div, table, 'result']

    def get_open_result_thing_price(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoThngPreparPcDetail'
        table = 'raw_open_result_thing_price'
        div = {'1': None}
        return [url, div, table, None]

    def get_open_result_thing_successful(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getScsbidListSttusThng'
        table = 'raw_open_result_thing_successful'
        div = {'1': None}
        return [url, div, table, None]

    def get_open_result_service(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoServc'
        table = 'raw_open_result_service'
        div = {'1': None}
        return [url, div, table, 'result']

    def get_open_result_service_price(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoServcPreparPcDetail'
        table = 'raw_open_result_service_price'
        div = {'1': None}
        return [url, div, table, None]

    def get_open_result_service_successful(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getScsbidListSttusServc'
        table = 'raw_open_result_service_successful'
        div = {'1': None}
        return [url, div, table, None]

    def get_open_result_construction(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoCnstwk'
        table = 'raw_open_result_construction'
        div = {'1': None}
        return [url, div, table, 'result']

    def get_open_result_construction_price(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoCnstwkPreparPcDetail'
        table = 'raw_open_result_construction_price'
        div = {'1': None}
        return [url, div, table, None]

    def get_open_result_construction_successful(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getScsbidListSttusCnstwk'
        table = 'raw_open_result_construction_successful'
        div = {'1': None}
        return [url, div, table, None]

    def get_open_result_info(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoOpengCompt'
        table = 'raw_open_result_info'
        return [url, table]

    def get_open_result_fail_info(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoFailing'
        table = 'raw_open_result_fail_info'
        return [url, table]

    def get_open_result_rebid_info(self):
        url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoRebid'
        table = 'raw_open_result_rebid_info'
        return [url, table]

    def get_demand(self):
        url = 'http://apis.data.go.kr/1230000/UsrInfoService/getDminsttInfo'
        table = 'raw_demand'
        div = {'1': None, '2': 'rgstDt'}
        return [url, div, table, None]

    def get_corporation(self):
        url = 'http://apis.data.go.kr/1230000/UsrInfoService/getPrcrmntCorpBasicInfo'
        table = 'raw_corporation'
        div = {'1': None, '2': 'rgstDt'}
        return [url, div, table, 'corporation']

    def get_corporation_industry(self):
        url = 'http://apis.data.go.kr/1230000/UsrInfoService/getPrcrmntCorpIndstrytyInfo'
        table = 'raw_corporation_industry'
        return [url, table]

    def get_corporation_product(self):
        url = 'http://apis.data.go.kr/1230000/UsrInfoService/getPrcrmntCorpSplyPrdctInfo'
        table = 'raw_corporation_product'
        return [url, table]

    def get_product2(self):
        url = 'http://apis.data.go.kr/1230000/ThngListInfoService/getPrdctClsfcNoUnit2Info'
        table = 'raw_product2'
        return [url, table]

    def get_product4(self):
        url = 'http://apis.data.go.kr/1230000/ThngListInfoService/getPrdctClsfcNoUnit4Info'
        table = 'raw_product4'
        return [url, table]

    def get_product6(self):
        url = 'http://apis.data.go.kr/1230000/ThngListInfoService/getPrdctClsfcNoUnit6Info'
        table = 'raw_product6'
        return [url, table]

    def get_product8(self):
        url = 'http://apis.data.go.kr/1230000/ThngListInfoService/getPrdctClsfcNoUnit8Info'
        table = 'raw_product8'
        return [url, table]

    def get_product10(self):
        url = 'http://apis.data.go.kr/1230000/ThngListInfoService/getPrdctClsfcNoUnit10Info'
        table = 'raw_product10'
        return [url, table]

    def get_industry(self):
        url = 'http://apis.data.go.kr/1230000/IndstrytyBaseLawrgltInfoService/getIndstrytyBaseLawrgltInfoList'
        table = 'raw_industry'
        return [url, table]

    def get_LH_announce(self):
        url = 'http://openapi.ebid.lh.or.kr/ebid.com.openapi.service.OpenBidInfoList.dev'
        table = 'raw_lh_announce'
        div = {'1': None}
        return [url,table]

    def get_LH_result(self):
        url = 'http://openapi.ebid.lh.or.kr/ebid.com.openapi.service.OpenTenderopenList.dev'
        table = 'raw_lh_result'
        div = {'1': None}
        return [url,table]
