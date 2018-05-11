# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import hashlib
import json
import random
import base64
import requests
import time
from fake_useragent import UserAgent
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

# HttpIpPool
class HttpIpPoolProxyMiddleware(object):
    def process_request(self, request, spider):
        while True:
            try:
                response = requests.get('IP接口').content  # IP代理的接口
            except Exception:
                pass
            else:
                jo = json.loads(response)
                proxies_ip = jo['ip']
                request.meta['proxy'] = 'http://{}'.format(proxies_ip)
                break
        return None


# 随机User_Agent
class ProcessHeaderMidware():
    """process request add request info"""

    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):

        """
        随机从列表中获得header， 并传给user_agent进行使用
        """
        if "IsPhone" in request.meta.keys() and request.meta['IsPhone'] == 1:
            ua = random.choice(settings.get('USER_AGENT_LIST'))
            if ua:
                request.headers['User-Agent'] = ua
        else:
            request.headers['User-Agent'] = self.ua.random
        if "retry_time" not in request.meta.keys():
            request.meta['retry_time'] = 1
        pass
