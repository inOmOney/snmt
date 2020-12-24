import requests
import time

class Sn_Reserve(object):
    def __init__(self):
        pass

    def reserve(self):
        #'https://product.suning.com/0000000000/11001203841.html'
        #preBuyCallback({"status":0,"code":"00","message":"恭喜您预约成功！","newCode":"00","newMessage":"恭喜您预约成功！","value":{"rushStartTime":"2020-12-25 09:30:00","phoneNumber":"","primaryName":"查看我的预约","primaryUrl":"https://yushou.suning.com/appoint/myAppoint.do","secondaryName":"","secondaryUrl":""}})
        #preBuyCallback({"status":0,"code":"006","message":"您已预约过,无需重复预约！","newCode":"006","newMessage":"您已预约过,无需重复预约！","value":{"rushStartTime":"2020-12-25 09:30:00","phoneNumber":"","primaryName":"查看我的预约","primaryUrl":"https://yushou.suning.com/appoint/myAppoint.do","secondaryName":"","secondaryUrl":""}})
        m_time = int(time.time() * 1000)
        url = 'https://yushou.suning.com/jsonp/appoint/gotoAppoint_202012210021_000000011001203841_0000000000_P01_1_preBuyCallback.do?callback=preBuyCallback&referenceURL=https%3A%2F%2Fproduct.suning.com%2F0000000000%2F11001203841.html&_={}'.format(m_time)
        resp = self.session.get(url=url)
        resp_json = self.cont.parse_json(resp.text)
        print(resp_json)


    def main(self, session, cont):
        self.session = session
        self.cont = cont
        sn_res.reserve()

sn_res = Sn_Reserve()
