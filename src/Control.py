import requests
import json
from src.config import Config
from src.logger import logger
from src.sn_reserve import Sn_Reserve
from src.sn_sell import Sn_Sell

sn_res = Sn_Reserve()
sn_sell = Sn_Sell()

class Control(object):
    def __init__(self):
        pass

    def session(self):
        session = requests.session()
        url = 'https://product.suning.com/pds-web/ajax/newRxfFunc_000000012132976441_0071234845__1.html'
        session.headers = {
            'User-Agent': 'Mozil.la/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Host': 'product.suning.com',
            'Connection': 'keep-alive',
            'Cookie': '{}'.format('config'),
        }
        payload = {
            'eppProductCode': '01011000126',
        }
        resp = session.post(
            url=url, params=payload, allow_redirects=False)
        print(resp.text)
        if resp.status_code == requests.codes.OK:
            logger.info('校验是否登录[成功]')
        else:
            logger.info("Error")

        url2 = 'https://my.suning.com/person.do?safp=d488778a.ddlb.AVsm.2&safpn=10009'




    def main(self, num):
        con = Control()
        con.session()
