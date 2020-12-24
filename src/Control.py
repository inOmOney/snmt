import requests
import json
import time
import sys
from lxml import etree
from src.config import config
from src.logger import logger
from src.sn_reserve import sn_res
from src.sn_sell import sn_sell

class Control(object):
    def __init__(self):
        self.session = self.session()
        self.UA = config.get_UA()

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
        m_url = 'https://my.suning.com/person.do'
        
        headers = {
            'User-Agent': self.UA(),
            'Host': 'my.suning.com',
            'Referer': 'https://order.suning.com/order/orderList.do?safp=d488778a.homepagev8.Ygnh.1&safpn=10001',
        }

    def reserve(self):
        for n in range(1, 3):
            try:
                m_time = int(time.time() * 1000)
                m_url = 'https://order.suning.com/order/orderList.do'
                resp = self.session.get(url=m_url)
                if resp.status_code == requests.codes.OK:
                    logger.info('校验是否登录[成功]')
                    logger.info('用户:{}'.format(self.get_username()))
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
        #preBuyCallback({"status":0,"code":"00","message":"恭喜您预约成功！","newCode":"00","newMessage":"恭喜您预约成功！","value":{"rushStartTime":"2020-12-25 09:30:00","phoneNumber":"","primaryName":"查看我的预约","primaryUrl":"https://yushou.suning.com/appoint/myAppoint.do","secondaryName":"","secondaryUrl":""}})
        #preBuyCallback({"status":0,"code":"006","message":"您已预约过,无需重复预约！","newCode":"006","newMessage":"您已预约过,无需重复预约！","value":{"rushStartTime":"2020-12-25 09:30:00","phoneNumber":"","primaryName":"查看我的预约","primaryUrl":"https://yushou.suning.com/appoint/myAppoint.do","secondaryName":"","secondaryUrl":""}})

    def main(self, num):
        self.reserve()
        if num == '1':
            pass
            #sn_res.main(self.session, cont)
        elif num == '2':
            """
            for(3)
            pool work = 3
            sn_sell.main()
            """
            sn_sell.main(self.session)

cont = Control()
