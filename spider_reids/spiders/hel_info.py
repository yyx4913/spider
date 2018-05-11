# -*- encoding: utf-8 -*-
import re,redis
import time,requests
# from copy import deepcopy
from lxml import etree
from datetime import datetime
from scrapy.exceptions import DontCloseSpider, CloseSpider
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from spider_redis.items import WuBaDetailItem
import random

# 家政/休闲/娱乐
class HelInfoSpider(RedisSpider):
    name = 'hel_info'
    allowed_domains = ['58.com']
    redis_key = 'hel_info:start_urls'
    num_rest = 0
    rdm = ['a','b','c','d','e','f','g','m','k','n']
    types = ['shenghuo', 'xiuxianyl', 'liren']
    custom_settings = {
        'REDIS_PARAMS': {  # redis 
            'password': '***',
            'db': ***
        },
        'ITEM_PIPELINES': {
            'spider_redis.pipelines.WuBaPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_redis.middlewares.ProcessHeaderMidware': 111,
            # 在中间件中设置代理ip
        },
        'RETRY_TIMES': 3,
        'DOWNLOAD_TIMEOUT': 30,
        # 'REDIRECT_ENABLED': False,
        # 'HTTPERROR_ALLOWED_CODES': [404],
        'CONCURRENT_REQUESTS': '64',
        # 'CONCURRENT_REQUESTS_PER_IP': '1',
        # 'DOWNLOAD_DELAY': 0.2,
        'LOG_FILE': './logs/hel_info.logs',
        'LOG_FORMAT': '%(name)s-%(levelname)s: %(message)s',
        'LOG_LEVEL': 'ERROR'
    }

    def parse(self, response):  # 获取城市列表
        self.num_rest = 0
        cities = re.findall(r'".*?":"(\w*?)\|.*?"', response.body)
        for city in cities[4:len(cities)]:
            # if 'hz' != city:   #杭州
            for ty in self.types:
                url = 'http://{}.58.com/{}.shtml'.format(city,ty)
                yield Request(url=url, callback=self.first_info)
            # else:
            #     pass

    def first_info(self, response):
        home_url = 'http://' + response.url.split('/')[2]  # http://hz.58.com
        jx = response.xpath('//dt/a/@href').extract() # 家政/休闲
        xx = response.xpath(u'//a[text()="室内休闲"]/../following-sibling::*/a/@href').extract() # 室内休闲
        urls = jx + xx
        if urls:
            for m_kind in urls:
                url = home_url + m_kind
                yield Request(url=url, callback=self.second_info,
                              meta={'home_url': home_url, 'm_kind': m_kind, 'retry_time': 0, 'req_url':url})
        else:  # 丽人/公共服务
            lr = response.xpath('//div[@class="cb mb50"]//h2/a/@href').extract()
            for url in lr:
                m_kind = '/' + url.split('/')[3] + '/' if len(url.split('/')) == 5 else ''
                yield Request(url=url, callback=self.second_info,
                              meta={'home_url': home_url, 'm_kind': m_kind, 'retry_time': 0, 'req_url':url})

    def second_info(self,response):  # 按照地区划分url
        self.num_rest = 0
        req_url = response.meta['req_url']
        home_url = response.meta['home_url']
        m_kind = response.meta['m_kind']  # 大分类
        retry_time = response.meta['retry_time']
        area_urls = response.xpath('//dd[@id="local"]/a/@href').extract()  # 地区
        if not area_urls and retry_time < 6: # 出现验证码
            proxies = response.meta['proxy']
            ip = re.search(r'http://(.*)', proxies, re.M | re.I)
            yield Request(url=req_url, callback=self.second_info, errback=self.log_err, meta={'retry_time': retry_time+1,
                                                                                          'home_url': home_url,
                                                                                          'm_kind': m_kind,'req_url':req_url})
        elif '/bianminfw.shtml' in response.url: # 公共服务
            yield Request(url=response.url, callback=self.first_info,dont_filter=True)
        elif area_urls:
            kinds = response.xpath('//dd[@id="ObjectType"]/a/@href').extract() # 类别1
            phones = response.xpath('//dd[@id="shoujipinpai"]/a/@href').extract() # 手机维修分类
            kind_urls = kinds if kinds else phones
            if area_urls:
                for area_url in area_urls[1:]:
                    area_url = area_url.split('/')[1] if len(area_url.split('/')) == 4 else area_url
                    if kind_urls:
                        for kind_url in kind_urls[1:]:
                            kind = kind_url.split('/')[3] if len(kind_url.split('/')) == 5 else ''
                            url = home_url + '/'+ area_url +'/' + kind
                            yield Request(url=url, callback=self.third_info,  errback=self.log_err, meta={'home_url': home_url, 'm_kind':m_kind,
                                                                                                          'retry_time':retry_time, 'req_url':url})
                    else:
                        url = home_url + '/' + area_url + m_kind
                        yield Request(url=url, callback=self.third_info,  errback=self.log_err, meta={'home_url': home_url, 'm_kind':m_kind,
                                                                                                      'retry_time':retry_time,'req_url':url})
            else:
                return
        else:
            self.logger.error('second url is %s, code is %s', response.url, response.status)

    def third_info(self,response):
        self.num_rest = 0
        req_url = response.meta['req_url']
        home_url = response.meta['home_url']
        m_kind = response.meta['m_kind']
        retry_time = response.meta['retry_time']
        list_urls = response.xpath('//div[@class="item-desc"]/preceding-sibling::a[1]/@href').extract()
        if 'callback' in response.url and retry_time < 5:
            proxies = response.meta['proxy']
            ip = re.search(r'http://(.*)', proxies, re.M | re.I)
            yield Request(url=req_url, callback=self.third_info, errback=self.log_err, meta={'home_url': home_url,
                                                                                         'm_kind': m_kind,
                                                                                         'retry_time': retry_time+1,'req_url':req_url})
        elif list_urls:
            for url in list_urls:
                res = re.findall(r'.*?entinfo=(.*?)_.*?', url)
                if res:
                    detail_url = home_url + m_kind + res[0] + 'x.shtml'
                else:
                    detail_url = url
                yield Request(url=detail_url, callback=self.detail, errback=self.log_err,
                          meta={'detail_url': detail_url,
                                'retry_time': retry_time,
                                'm_kind': m_kind, 'home_url': home_url})
            next_url = response.xpath("//a[@class='next']/@href").extract_first()
            if next_url:
                page_url = home_url + next_url + '?PGTID=0d30{}-{}-&ClickID={}'.format(
                    ''.join(random.sample(self.rdm, 4)),
                    ''.join(random.sample(self.rdm, 4)),
                    str(random.randint(1, 9)))
                yield Request(url=page_url, callback=self.third_info, errback=self.log_err, meta={'home_url': home_url,
                                                                                                  'retry_time': 0,
                                                                                                  'm_kind': m_kind,
                                                                                                  'req_url': page_url})
        elif '.shtml' in response.url:
            yield Request(url=response.url, callback=self.detail, errback=self.log_err,
                      meta={'detail_url': response.url,
                            'retry_time': retry_time,
                            'm_kind': m_kind, 'home_url': home_url})
        else:
            self.logger.error('third url is %s has no list', response.url)
            return

    def detail(self, response):
        self.num_rest = 0
        shop_url = response.meta['detail_url']
        retry_time = response.meta['retry_time'] if 'retry_time' in response.meta else 0
        if 'callback.58.com/' in response.url and retry_time<6: #验证码
            proxies = response.meta['proxy']
            ip = re.search(r'http://(.*)', proxies, re.M | re.I)
            detail_url = re.findall(r'com%2F(.*)', response.url)
            if detail_url:
                urls = detail_url[0].split('%2F')
                url = 'http://' + urls[0] +'.58.com/'+urls[1] + '/'+ urls[2]
                yield Request(url=url, callback=self.detail, errback=self.log_err,
                          meta={'retry': retry_time + 1,'detail_url': shop_url})
            else:
                pass
        elif 'http://m' in response.url and retry_time<6: # 跳转手机页面
            m_url = response.url.split('?')[0]
            m_url = m_url.split('/')
            if len(m_url) == 6:
                url = 'http://'+ m_url[3]+'.58.com/'+ m_url[4] +'/'+ m_url[5]
                yield Request(url=url, callback=self.detail, errback=self.log_err,
                              meta={'retry': retry_time + 1,'detail_url': shop_url})
            else:
                return
        else:
            map_list = re.findall(
                r'"lat":"(.*?)","bsName":"(.*?)".*?"districtName":"(.*?)","cateName":"(.*?)".*?"cityName":"(.*?)","lng":"(.*?)","area":"(.*?)"',
                response.body)
            if map_list and map_list[0] and map_list[0][5]:
                item = WuBaDetailItem()
                item['shop_url'] = shop_url
                item['shop_name'] = response.xpath("//div[@class='userinfo']//h2/text()").extract_first()
                item['hot_num'] = response.xpath("//div[@class='userinfo']//li[1]/em/text()").extract_first()
                item['active_num'] = response.xpath("//div[@class='userinfo']//li[2]/em/text()").extract_first()
                item['service_grade'] =response.xpath("//div[@class='userinfo']//li[3]/em/text()").extract_first()
                item['tag_flag'] = '>'.join(response.xpath("//div[@class='nav']/a/text()").extract())
                item['map_lat'] = map_list[0][0]
                item['map_lng'] = map_list[0][5]
                item['city'] = map_list[0][4]
                item['cate'] = map_list[0][3]
                item['address'] = (map_list[0][2] + "-" + map_list[0][1] + "-" + map_list[0][6]).replace(u'，','&').replace(',','&')
                yield item
            else:
                return

    def log_err(self,failure):
        self.num_rest = 0
        if failure.check(HttpError):
            response = failure.value.response
            retry_time = response.meta['retry_time']
            if retry_time< 6:
                res_url = response.url.split('?')[0].split('/')
                if '/pn' in response.url or len(res_url) == 6:
                    home_url = response.meta['home_url']
                    m_kind = response.meta['m_kind']
                    req_url = response.meta['req_url'] if 'req_url' in response.meta else response.url
                    yield Request(url=response.url, callback=self.third_info,dont_filter=True, meta={ 'retry_time':retry_time+1,
                                                                                                      'm_kind':m_kind,'home_url':home_url,
                                                                                                      'req_url':req_url})
                elif 'shtml' in response.url:
                    shop_url = response.meta['detail_url']
                    yield Request(url=shop_url, callback=self.detail, errback=self.log_err, dont_filter=True,meta={'detail_url':shop_url,
                                                                                                                  'retry_time':retry_time+1})
                elif len(res_url) ==5:
                    home_url = response.meta['home_url']
                    m_kind = response.meta['m_kind']
                    req_url = response.meta['req_url'] if 'req_url' in response.meta else response.url
                    yield Request(url=response.url, callback=self.second_info, dont_filter=True, errback=self.log_err,
                                  meta={'retry_time':retry_time+1,'m_kind':m_kind,'home_url':home_url,'req_url':req_url})
                else:
                    self.logger.error('HttpError on %s:%s ,%s', response.url, response.status, datetime.now())
            else:
                self.logger.error('HttpError on %s:%s ,%s', response.url, response.status, datetime.now())
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s:%s', request.url, datetime.now())
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            retry_time = request.meta['retry_time'] if 'retry_time' in request.meta else 0
            if retry_time < 6:
                res_url = request.url.split('?')[0].split('/')
                if '/pn' in request.url or len(res_url) == 6:
                    home_url = request.meta['home_url']
                    m_kind = request.meta['m_kind']
                    req_url = request.meta['req_url'] if 'req_url' in request.meta else request.url
                    yield Request(url=request.url, callback=self.third_info,dont_filter=True, meta={ 'retry_time':retry_time+1,
                                                                                                      'm_kind':m_kind,'home_url':home_url,
                                                                                                     'req_url':req_url})
                elif 'shtml' in request.url:
                    shop_url = request.meta['detail_url'] if 'detai_url' in request.meta else request.url
                    yield Request(url=shop_url, callback=self.detail, errback=self.log_err, dont_filter=True,meta={'detail_url':shop_url,
                                                                                                                   'retry_time':retry_time+1})
                elif len(res_url) ==5:
                    home_url = request.meta['home_url']
                    m_kind = request.meta['m_kind']
                    req_url = request.meta if 'req_url' in request.meta else request.url
                    yield Request(url=request.url, callback=self.second_info, dont_filter=True, errback=self.log_err,
                                  meta={'retry_time':retry_time+1,'m_kind':m_kind,'home_url':home_url, 'req_url':req_url})
                else:
                    self.logger.error('TimeoutError on %s,%s,%s', request.url, retry_time, datetime.now())

            else:
                self.logger.error('TimeoutError on %s,%s,%s', request.url, retry_time, datetime.now())
        else:
            pass



    def spider_idle(self):
        self.num_rest += 1
        if self.num_rest < 100:
            self.schedule_next_requests()
            raise DontCloseSpider
        else:
            print("spider closed !")
            raise CloseSpider