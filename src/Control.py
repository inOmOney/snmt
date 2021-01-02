import requests
import json
import time
import sys
import random
from urllib import parse
from lxml import etree
from src.config import config
from src.logger import logger
from src.sn_reserve import sn_res
from src.sn_sell import sn_sell

class Control(object):

    def __init__(self):
        self.UA = config.get_UA()
        self.session = self.session()
        data = dict()
        cartvo = dict()

    def get_cookies(self):
        manual_cookies = {}
        for item in config.getRaw('config', 'cookies_String').split(';'):
            name, value = item.strip().split('=', 1)
            # 用=号分割，分割1次
            manual_cookies[name] = value
            # 为字典cookies添加内容
        cookiesJar = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None, overwrite=True)
        return cookiesJar

    def parse_json(self, m_str):
        begin = m_str.find('{')
        end = m_str.rfind('}') + 1
        return json.loads(m_str[begin:end])

    def session(self):
        session = requests.session()
        session.headers = {
            'User-Agent': '{}'.format(self.UA),
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        session.cookies = self.get_cookies()
        #checksession
        checksession = requests.session()
        checksession.headers = {
            'User-Agent': '{}'.format(self.UA),
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        session.cookies = self.get_cookies()
        return session

    def get_username(self):
        #m_url = 'https://my.suning.com/person.do'
        m_url = 'https://myapi.suning.com/api/member/queryContactInfos.do'

        headers = {
            'Host': 'myapi.suning.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0(Linux; U;SNEBUY-APP;9.3.6-387;SNCLIENT; Android 5.1.1; zh; ELE-AL00) AppleWebKit/533.0 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 maa/2.1.2',
        }

        resp = self.session.get(url=m_url)
        if resp.status_code == requests.codes.OK:
            logger.info('登录成功')
            print(resp.text)


    def reserve(self):
        for n in range(1, 3):
            try:
                """
                1. {"status":0,"code":"00","message":"恭喜您预约成功！","newCode":"00","newMessage":"恭喜您预约成功！"}
                2. checkPurchasableCallback({"status":0,"code":"00","message":"用户已预约","newCode":null,"newMessage":null,"pointsThreshold":0})
                3. preBuyCallback({"status":0,"code":"00","message":"恭喜您预约成功！","newCode":"00","newMessage":"恭喜您预约成功！","value":{"rushStartTime":"2020-12-25 09:30:00","phoneNumber":"","primaryName":"查看我的预约","primaryUrl":"https://yushou.suning.com/appoint/myAppoint.do","secondaryName":"","secondaryUrl":""}})
                4. preBuyCallback({"status":0,"code":"006","message":"您已预约过,无需重复预约！","newCode":"006","newMessage":"您已预约过,无需重复预约！","value":{"rushStartTime":"2020-12-25 09:30:00","phoneNumber":"","primaryName":"查看我的预约","primaryUrl":"https://yushou.suning.com/appoint/myAppoint.do","secondaryName":"","secondaryUrl":""}})
                5. '{"status":0,"code":"-1","message":"预约失败，请您重试！[015]","newCode":null,"newMessage":null,"value":null}
                """
                m_url = 'https://yushou.suning.com/jsonp/appoint/gotoAppoint_202012240023_000000011001203841_0000000000_P01_2_submissionAppointments.do'
                headers = {
                    'Host': 'yushou.suning.com',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'Mozilla/5.0(Linux; U;SNEBUY-APP;9.3.6-387;SNCLIENT; Android 5.1.1; zh; ELE-AL00) AppleWebKit/533.0 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 maa/2.1.2',
                }
                resp = self.session.get(url=m_url)
                if resp.status_code == requests.codes.OK:
                    logger.info(("预约成功"))
                    #logger.info('校验是否登录[成功]')
                    #logger.info('用户:{}'.format(self.get_username()))
                    return True
                else:
                    logger.info('校验是否登录[失败]')
                    logger.info('请重新输入cookie')
                    time.sleep(1)
                    continue
            except Exception as e:
                logger.info('第【%s】次失败请重新获取cookie', n)
                time.sleep(1)
                continue
        sys.exit(1)
        #'https://product.suning.com/0000000000/11001203841.html'

    def get_cart_vo(self):
        self.jq = 'jQuery{}'.format(random.randint(1000000, 9999999)) + "_" + self.jqtime
        self.cart_vo = '{"provinceCode":"120","cityCode":"531","districtCode":"53101",' \
                       '"cmmdtyVOList":[{"cmmdtyCode":"000000010672048887","shopCode":"0070733525","activityType":"26","cmmdtyQty":"2","activityId":"20201231093945017",' \
                       '"collect":[{"collectSort":"10","collectType":"12","collectCode":"page_id=10004;mod_id=22;eleid=140000530;site_id=d488778a"},' \
                       '{"collectSort":"10","collectType":"13","collectCode":"pgcate=10008;prdtp=00027;tag=;pgtitle=普通四级页;prdid=10672048887;shopid=0070733525;supid=0070733525"}]}],' \
                       '"townCode":"5310199","verifyCode":"","uuid":"","sceneId":"",' \
                       '"dfpToken":"THSkhh176be820997FAww7033"}'
        


    def buy(self):
        url = 'https://shopping.suning.com/addCart.do?'

        headers = {
            "User-Agent": self.UA,
            "Host": "shopping.suning.com",
            "Referer": "https://product.suning.com/0070733525/10672048887.html",
        }

        self.data2 = '%7B%22provinceCode%22%3A%22120%22%2C%22cityCode%22%3A%22531%22%2C%22districtCode%22%3A%2253101%22%2C%22cmmdtyVOList%22%3A%5B%7B%22cmmdtyCode%22%3A%22000000010672048887%22%2C%22shopCode%22%3A%220070733525%22%2C%22activityType%22%3A%2226%22%2C%22cmmdtyQty%22%3A%221%22%2C%22activityId%22%3A%2220201231093945017%22%2C%22collect%22%3A%5B%7B%22collectSort%22%3A%2210%22%2C%22collectType%22%3A%2212%22%2C%22collectCode%22%3A%22page_id%3D10004%3Bmod_id%3D22%3Beleid%3D140000530%3Bsite_id%3Dd488778a%22%7D%2C%7B%22collectSort%22%3A%2210%22%2C%22collectType%22%3A%2213%22%2C%22collectCode%22%3A%22pgcate%3D10008%3Bprdtp%3D00027%3Btag%3D%3Bpgtitle%3D%E6%99%AE%E9%80%9A%E5%9B%9B%E7%BA%A7%E9%A1%B5%3Bprdid%3D10672048887%3Bshopid%3D0070733525%3Bsupid%3D0070733525%22%7D%5D%7D%5D%2C%22townCode%22%3A%225310199%22%2C%22verifyCode%22%3A%22%22%2C%22uuid%22%3A%22%22%2C%22sceneId%22%3A%22%22%2C%22dfpToken%22%3A%22THSkhh176be820997FAww7033___w7DDp8KdwqVLw5wZbMOxKmfCrMOMDsOKw7FawqnCt8Ou%22%7D'
        payload = {
            'callback': self.jq,
            '_': self.jqtime,
            'cart_vo': self.data2,
        }

        resp = self.session.get(url=url, headers=headers, params=payload)
        print(1)
        "17207375182994757352"
        "17207014311137139606"

    def tbuy(self):
        url = 'https://product.suning.com/0000000000/11190081412.html'
        turl = 'https://shopping.suning.com/app/cart1/gateway/addCmmdty.do'
        headers = {
            'Host': 'shopping.suning.com',
            'Connection': 'Keep-Alive',
            'sn_page_source': '',
            'hiro_trace_id': '3036cbd50cf143479cfe0c4e25c49a6a',
            'snTraceId': '3036cbd50cf143479cfe0c4e25c49a6a',
            'User-Agent': 'Mozilla/5.0(Linux; U;SNEBUY-APP;9.5.4-396;SNCLIENT; Android 5.1.1; zh; ELE-AL00) AppleWebKit/533.0 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 maa/2.2.2',
        }
        dfptoken = "THh7je176c156cf77PJnp1d88"
        data = dict()
        data = "%7B%22cartHeadInfo%22%3A%7B%22tempCartId%22%3A%22%22%2C%22customerNo%22%3A%22%22%2C%22userFlag%22%3A%220%22%2C%22operationChannel%22%3A%2250%22%2C%22operationTerminal%22%3A%2201%22%2C%22operationEquipment%22%3A%2202%22%2C%22operationUser%22%3A%22%22%2C%22operationStoreCode%22%3A%22%22%2C%22token%22%3A%22d88392aa-0483-48e0-ad5f-5e0c9a09a273%22%2C%22dfpToken%22%3A%22TFEppU81ycj9cVkyyGdKbb7cd___w7DDqcKLwr5Tw6EZbMOxKmfCrMOEBcOGw7xbwqLCs8Ol%22%2C%22detect%22%3A%22mmds_a_._907fe204-f4aa-4dfe-b49e-98f80685b8f0_._bEEE33YI4goKgM3333G0X0133333HpS_u3333Lw533333333YI4TK7gB3o*McbD01333333333YgB33YjGbD013333YI4TK7h8Yj6zcDu013333YI4hlZh833YHGDu0133333mYSvs3333DN5333333333HpS_u3333M4533333333YI4TK7hh3Y6pcFY013333YI4hlZhh3335GFY0133333mYSvs3333Ff5333333333HpS_u333Yej533333333YI4TK7hF3Y7bcDh013333YI4hlZhF333_GDh0133333mYSvs33339B5333333333HpS_u3333rG533333333YI4TK7hFY-lncFT013333YI4hlZhF33YLGFT0133333mYSvs3333D2533333333YI4TlBYJ33Qlcbf013333YI4TjlYJ33YfGbf013333YI4TlBhg33Hlc3S013333YI4Tk1hg33Y0G3S013333YI4TlBhc33a8cbU013333YI4ik-hc33YXGbA0133333HpS_u3333WV533333333YI4TK7ha33jLcbK01333333333Yha333oGbK013333YI4TK7hF3YN.caO01333333333YhF33YgGaO013333YI4TK7hH3YbXcD*013333YI4hlZhH33YKGD*0133333mYSvs33339k533333333YI4TlBYJ3Y32cb_013333YI4TjlYJ333NGb_013333YI4TlBhF33eFc3M013333YI4Tk1hF33Y9G3M013333YI4TlBgP33a8ccg013333YI4ik-g233YTGck0133333HpS_u3333-X533333333YI4TK7he3YLJcbf01333333333Yhe3335Gbd013333YI4TK7h43tU9cFX013333YI4hlZh033YbGFX0133333mYSvs3333D55333333333HpS_u33332k533333333YI4TK7hg3DlvcD-013333YI4hlZhg33YdGD-0133333mYSvs3333F2533333333YI4TlBY83YDvcb_013333YI4TjlY833YXGb_013333YI4TlBhF33jtc3W013333YI4Tk1hF33YiG3W013333YI4TlBhc33c.ca5013333YI4ik-hc3334Ga50133333HpS_u3333wj533333333YI4TK7hh3XKscD-013333YI4hlZhh33YFGD-0133333mYSvs33334Q5333333333HpS_u3333sy533333333YI4TK7hF3NgucD*013333YI4hlZhF33YZGD*0133333mYSvs3333DP5333333333HpS_u3333MS533333333YI4TK7hX33hWcFb013333YI4hlZhX33YDGFb0133333mYSvs3333DA533333333YI4TlBYN33jdcbK013333YI4TjlYN33YTGbK013333YI4TlBhH33gvc32013333YI4Tk1hH33YuG32013333YI4TlBhX33dacbs013333YI4ik-hX3332Gbs0133333HpS_u33338G533333333YI4TK7he3VSbcDU013333YI4hlZhH33YDGDU0133333mYSvs3333DU5333333333HpS_u33335T533333333YI4TK7h33eckcaJ01333333333Yh333YhGaJ0133EEEUBNoNK2vlmEEE344Z3Xl3AZg3GlleghGXVgxemxAXAx4GEEE3XbT44B1zzEEEbXXREEE4EEEX3xxReXeEEEXExEGEEE4xTe3eA33bT43EEERTTAAxe33GEEE906438d491ca8cd00108a8c73a3df328%22%2C%22provinceCode%22%3A%22120%22%2C%22cityCode%22%3A%22531%22%2C%22districtCode%22%3A%2253111%22%2C%22townCode%22%3A%22%22%2C%22sourcePageType%22%3A%2201%22%2C%22encryFlag%22%3A%221%22%2C%22logContent%22%3A%22%22%2C%22deviceNo%22%3A%22wB0qKQaiV6yll2sawmhFqA**%22%2C%22terminalVersion%22%3A%22MOBILE%7C02%7C01%7C9.5.4%7C11010%22%2C%22appVersions%22%3A%2201%22%2C%22platform%22%3A%2201%22%2C%22poiId%22%3A%221911100006617531%22%2C%22channelType%22%3A%2202%22%7D%2C%22historyPayType%22%3A%7B%22payType%22%3A%22%22%2C%22payPeriods%22%3A%22%22%7D%2C%22cmmdtyInfos%22%3A%5B%7B%22cmmdtyHeadBasicInfo%22%3A%7B%22itemNo%22%3A%221%22%2C%22activityType%22%3A%2202%22%2C%22subActivityType%22%3A%221%22%2C%22activityId%22%3A%2223312458%22%7D%2C%22mainCmmdtyInfo%22%3A%7B%22mainCmmdtyBasicInfo%22%3A%7B%22itemNo%22%3A%221%22%2C%22tickStatus%22%3A%221%22%2C%22cmmdtyCode%22%3A%22000000011190081412%22%2C%22shopAddCode%22%3A%220030000756%22%2C%22cmmdtyName%22%3A%22%E4%BA%94%E7%B2%AE%E6%B6%B2+%E6%99%AE%E4%BA%94+%E7%AC%AC%E5%85%AB%E4%BB%A3+%E7%BB%8F%E5%85%B8+52%E5%BA%A6500ml+%E5%8D%95%E7%93%B6%E8%A3%85+%E6%B5%93%E9%A6%99%E5%9E%8B%E7%99%BD%E9%85%92%22%2C%22shopCode%22%3A%220000000000%22%2C%22shopName%22%3A%22%E8%8B%8F%E5%AE%81%E8%87%AA%E8%90%A5%22%2C%22overSeasFlag%22%3A%22%22%2C%22cmmdtyQty%22%3A%222%22%2C%22serviceStoreCode%22%3A%22%22%2C%22serviceStoreName%22%3A%22%22%2C%22commodityType%22%3A%22%22%2C%22isOneHour%22%3A%22%22%2C%22productType%22%3A%22%22%7D%2C%22collect%22%3A%5B%7B%22collectSort%22%3A%2210%22%2C%22collectType%22%3A%2213%22%2C%22collectCode%22%3A%22pgcate%3D10008%3Bprdtp%3D00027%3Btag%3D%E5%9B%9B%E7%BA%A7%E9%A1%B5%3Bpgtitle%3D%E5%9B%9B%E7%BA%A7%E9%A1%B5%3Bprdid%3D000000011190081412%3Bshopid%3D0030000756%3Bsupid%3D0010313348%22%7D%2C%7B%22collectSort%22%3A%2210%22%2C%22collectType%22%3A%2212%22%2C%22collectCode%22%3A%22page_id%3D140%3Bmod_id%3D22%3Beleid%3D140006620%3Bsite_id%3D2cd5ed46%22%7D%5D%7D%7D%5D%2C%22supportYB%22%3A%221%22%2C%22publishDate%22%3A%2220201215%22%7D"

        print(type(data))
        data = str(data)
        url_data = parse.quote(data)
        #resp = self.session.post(url=turl, headers=headers, data=url_data)
        resp = self.session.post(url=turl, headers=headers, data=data)
        print(1)

        #"cmmdtyCode": "000000011001203841",
        #"shopAddCode": "0030000757",
        #"appcode": "0030000757"
        #数量"cmmdtyQty":"1"
        #"cmmdtyName": "飞天53%vol+500ml+贵州茅台酒（带杯）2020年产+酱香型白酒"

    def login(self):
        url = 'https://passport.suning.com/ids/qrLoginStateProbe'
        resp = self.session.get(url=url)
        print(1)

    def cbuy(self):
        #url = 'https://shopping.suning.com/app/addcart/gateway/addWapCmmdty.do'
        url = 'https://shopping.suning.com/app/cart1/gateway/addCmmdty.do'
        headers = {
            'Connection': 'keep-alive',
            'Host': 'shopping.suning.com',
            'Origin': 'https://m.suning.com',
            'Referer': 'https://m.suning.com/product/0000000000/11190081412.html?srcPoint=dacu_SCMS99hiniecopy71_20201201101032190442_01&safp=d488778a.SCMS99hiniecopy71.20201201101032190442.1&safc=prd.0.0&safpn=10002.00027',
        }

        data = dict()
        data = {"publishDate":"20200914","cmmdtyInfos":[{"cmmdtyHeadBasicInfo":{"itemNo":"1","activityType":"02","subActivityType":"","activityId":"23312458"},"mainCmmdtyInfo":{"mainCmmdtyBasicInfo":{"itemNo":"2","cmmdtyCode":"000000011190081412","shopCode":"0000000000","shopName":"苏宁自营","cmmdtyQty":"2","tickStatus":"1","overSeasFlag":"","cmmdtyName":"","serviceStoreCode":"","serviceStoreName":"","commodityType":""},"mainExtendInfos":[],"serveCodeItems":[],"contractBasic":{"contractDealType":"","selectedNum":"","mealId":"","monthlyFeeId":"","name":"","cardNum":"","phoneNum":""},"serveInsurance":[],"subCmmdtyItems":[],"collect":[{"collectSort":"10","collectType":"12","collectCode":"page_id=140;mod_id=10;eleid=140002000;site_id=f73ee1cf"},{"collectSort":"10","collectType":"13","collectCode":"pgtitle=普通四级页;pgcate=10008;prdtp=00027;tag=null/null;shopid=0030000756;prdid=000000011190081412;supid=0010313348"}]},"subCmmdtyInfos":[]}],"cartHeadInfo":{"operationTerminal":"01","operationChannel":"50","userFlag":"0","operationEquipment":"06","operationUser":"","operationStoreCode":"","sourcePageType":"01","provinceCode":"120","cityCode":"531","districtCode":"01","townCode":"5310199","channelType":"03","deviceNo":"160868704714487369","terminalVersion":"WAP|06","imageCode":"","uuid":"","dfpToken":"THFl8d176c1582358QkgYfa38___w7DDp8KIwqIbw5AZbMOxKmfCrMOEBMOAw7xYwqPCt8On","dareType":"","retailFormat":"","detect":"mmds_pL7owdanD5doq7ndwowsn7Lw_fpaTQ_pT_TQ_pTnnTLpq7n77_p_fpaT._kkkkkk._kk6Ekkkkkk4XkkQ2Nkkkkkbnkk-MkkkkkkCqNkTTCokkbNvMkkkk2GNkkkTqTdnpp_aaLLnTLTQqqoop7nnaTqTqqqqqqqLLL7qqoLaLfmd7fanL_fLLTaLaTQdKQREkXcjfuv2lE6TaLaTkNi032qSo5TaLaTQ_pTOUNkp23udfkkf2b5G4kkn3kuTs7n_QQoEdnqp_fqopn_._02c72446-b169-4f03-81fc-d59b5add8b6f_._"},"supportYB":"1"}
        
        data2 = "data=%7B%22publishDate%22%3A%2220200914%22%2C%22cmmdtyInfos%22%3A%5B%7B%22cmmdtyHeadBasicInfo%22%3A%7B%22itemNo%22%3A%221%22%2C%22activityType%22%3A%2202%22%2C%22subActivityType%22%3A%22%22%2C%22activityId%22%3A%2223312458%22%7D%2C%22mainCmmdtyInfo%22%3A%7B%22mainCmmdtyBasicInfo%22%3A%7B%22itemNo%22%3A%222%22%2C%22cmmdtyCode%22%3A%22000000011190081412%22%2C%22shopCode%22%3A%220000000000%22%2C%22shopName%22%3A%22%E8%8B%8F%E5%AE%81%E8%87%AA%E8%90%A5%22%2C%22cmmdtyQty%22%3A%222%22%2C%22tickStatus%22%3A%221%22%2C%22overSeasFlag%22%3A%22%22%2C%22cmmdtyName%22%3A%22%22%2C%22serviceStoreCode%22%3A%22%22%2C%22serviceStoreName%22%3A%22%22%2C%22commodityType%22%3A%22%22%7D%2C%22mainExtendInfos%22%3A%5B%5D%2C%22serveCodeItems%22%3A%5B%5D%2C%22contractBasic%22%3A%7B%22contractDealType%22%3A%22%22%2C%22selectedNum%22%3A%22%22%2C%22mealId%22%3A%22%22%2C%22monthlyFeeId%22%3A%22%22%2C%22name%22%3A%22%22%2C%22cardNum%22%3A%22%22%2C%22phoneNum%22%3A%22%22%7D%2C%22serveInsurance%22%3A%5B%5D%2C%22subCmmdtyItems%22%3A%5B%5D%2C%22collect%22%3A%5B%7B%22collectSort%22%3A%2210%22%2C%22collectType%22%3A%2212%22%2C%22collectCode%22%3A%22page_id%3D140%3Bmod_id%3D10%3Beleid%3D140002000%3Bsite_id%3Df73ee1cf%22%7D%2C%7B%22collectSort%22%3A%2210%22%2C%22collectType%22%3A%2213%22%2C%22collectCode%22%3A%22pgtitle%3D%E6%99%AE%E9%80%9A%E5%9B%9B%E7%BA%A7%E9%A1%B5%3Bpgcate%3D10008%3Bprdtp%3D00027%3Btag%3Dnull%2Fnull%3Bshopid%3D0030000756%3Bprdid%3D000000011190081412%3Bsupid%3D0010313348%22%7D%5D%7D%2C%22subCmmdtyInfos%22%3A%5B%5D%7D%5D%2C%22cartHeadInfo%22%3A%7B%22operationTerminal%22%3A%2201%22%2C%22operationChannel%22%3A%2250%22%2C%22userFlag%22%3A%220%22%2C%22operationEquipment%22%3A%2206%22%2C%22operationUser%22%3A%22%22%2C%22operationStoreCode%22%3A%22%22%2C%22sourcePageType%22%3A%2201%22%2C%22provinceCode%22%3A%22120%22%2C%22cityCode%22%3A%22531%22%2C%22districtCode%22%3A%2201%22%2C%22townCode%22%3A%225310199%22%2C%22channelType%22%3A%2203%22%2C%22deviceNo%22%3A%22160868704714487369%22%2C%22terminalVersion%22%3A%22WAP%7C06%22%2C%22imageCode%22%3A%22%22%2C%22uuid%22%3A%22%22%2C%22dfpToken%22%3A%22THFl8d176c1582358QkgYfa38___w7DDp8KIwqIbw5AZbMOxKmfCrMOEBMOAw7xYwqPCt8On%22%2C%22dareType%22%3A%22%22%2C%22retailFormat%22%3A%22%22%2C%22detect%22%3A%22mmds_pL7owdanD5doq7ndwowsn7Lw_fpaTQ_pT_TQ_pTnnTLpq7n77_p_fpaT._kkkkkk._kk6Ekkkkkk4XkkQ2Nkkkkkbnkk-MkkkkkkCqNkTTCokkbNvMkkkk2GNkkkTqTdnpp_aaLLnTLTQqqoop7nnaTqTqqqqqqqLLL7qqoLaLfmd7fanL_fLLTaLaTQdKQREkXcjfuv2lE6TaLaTkNi032qSo5TaLaTQ_pTOUNkp23udfkkf2b5G4kkn3kuTs7n_QQoEdnqp_fqopn_._02c72446-b169-4f03-81fc-d59b5add8b6f_._%22%7D%2C%22supportYB%22%3A%221%22%7D"

        resp = self.session.post(url=url, headers=headers, data=data2)
        print(1)


    def main(self, num):
        if num == '1':
            #self.get_useraddr()
            self.login()
            self.reserve()
        elif num == '2':
            self.jqtime = str(int(time.time() * 1000))
            #self.get_cart_vo()
            #self.buy()
            self.login()
            #self.tbuy()
            self.cbuy()
