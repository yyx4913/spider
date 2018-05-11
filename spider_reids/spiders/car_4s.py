# -*- coding: utf-8 -*-
import re
from scrapy.exceptions import DontCloseSpider, CloseSpider
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from zebra_spider_redis.items import CarFourItem

# 汽车之家 4s店
class CarFourSpider(RedisSpider):
    name = 'car_four'
    allowed_domains = ['dealer.autohome.com.cn']
    redis_key = 'car_four:start_urls'
    home_url = 'https://dealer.autohome.com.cn'
    num_rest = 0
    custom_settings = {
        'REDIS_PARAMS': {
            'password': '****',
            'db': ****
        },
        'ITEM_PIPELINES': {
            'zebra_spider_redis.pipelines.CarFourPipeline': 300,
            # 'scrapy_redis.pipelines.RedisPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'zebra_spider_redis.middlewares.ProcessHeaderMidware': 111,
            # 在中间件中设置代理ip
        },
        'RETRY_TIMES': 3,
        'DOWNLOAD_TIMEOUT': 30,
        # 'REDIRECT_ENABLED': False,
        # 'HTTPERROR_ALLOWED_CODES': [404],
        'CONCURRENT_REQUESTS': '64',
        # 'CONCURRENT_REQUESTS_PER_IP': '1',
        # 'DOWNLOAD_DELAY': 0.2,
        'LOG_FILE': './logs/car_four.logs',
        'LOG_FORMAT': '%(name)s-%(levelname)s: %(message)s',
        'LOG_LEVEL': 'ERROR'
    }

    def parse(self, response):
        self.num_rest = 0
        cities = re.findall(r'"Pinyin":"(.*?)",', response.text)
        for city in cities:
            url = self.home_url + '/' + city
            print url
            yield Request(url=url, callback=self.first_info, errback=self.err_log)

    def first_info(self, response):
        self.num_rest = 0
        list_divs = response.xpath('//li[@class="list-item"]')
        for list_div in list_divs:
            brand = list_div.xpath('./ul[@class="info-wrap"]/li[2]/span/em/text()').extract_first()
            car_num = list_div.xpath('./ul[@class="info-wrap"]/li[2]/a/text()').extract_first()
            level = list_div.xpath('./ul[@class="info-wrap"]//span[@class="icon-medal"]').extract_first()
            shop_url = list_div.xpath('./ul[@class="info-wrap"]/li[1]/a/@href').extract_first()
            url = 'https:' + shop_url
            yield Request(url=url, callback=self.second_info, meta={'brand':brand, 'car_num':car_num, 'level':level})

        page_num = re.findall(r'dealerCount = (.*?);', response.text)
        if page_num and 'pageIndex' not in response.url:
            i =2
            while i <= int(page_num[0]):
                url = response.url + '?pageIndex={}'.format(str(i))
                i +=1
                yield Request(url=url, callback=self.first_info, errback=self.err_log)

    def second_info(self, response):
        self.num_rest = 0
        res = re.findall(r'"MapLonBaidu":(.*?),"MapLatBaidu":(.*?),"MinistieName":"(.*?)","Address":"(.*?)",.*Phone":"(.*?)"'
                         r',"CityName":"(.*?)",', response.text)
        if res:
            brand_divs = response.xpath('//dl[@class="tree-dl"]')
            brand = []
            if brand_divs:
                for brand_div in brand_divs:
                    brand_dad = brand_div.xpath('./dt/a/text()').extract_first()
                    brand_son = brand_div.xpath('./dd/a/text()').extract()
                    final_res = brand_dad + ':' + '&'.join(brand_son)
                    brand.append(final_res)
            item = CarFourItem()
            item['city'] = res[0][5]
            item['shop_name'] = res[0][2]
            item['brand'] = response.meta['brand']
            num = re.findall('.*?(\d+).*', response.meta['car_num']) if response.meta['car_num'] else ''
            item['car_num'] = num[0] if num else 0
            level = re.findall(r'.*?<!--(.*?)-->.*',response.meta['level'])
            item['level'] = level[0] if level else ''
            item['address'] = res[0][3]
            item['lat'] = res[0][1]
            item['lng'] = res[0][0]
            item['phone'] = res[0][4]
            item['main_brand'] = ';'.join(brand)
            item['url'] = response.url
            yield item

    def err_log(self, failure):
        self.num_rest = 0
        if failure.check(HttpError):
            response = failure.value.response
            retry = response.meta['retry'] if 'retry' in response.meta else 0
            req_url = response.meta['req_url'] if 'req_url' in response.meta else response.url
            if retry < 6:
                retry +=1
                yield Request(url=response.url, callback=self.second_info, dont_filter= True, meta={'retry': retry, 'req_url': req_url})
            self.logger.error('HttpError on %s, status code %s', response.url, response.status)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            retry = request.meta['retry'] if 'retry' in request.meta else 0
            req_url = request.meta['req_url'] if 'req_url' in request.meta else request.url
            if retry < 6:
                retry += 1
                yield Request(url=req_url, callback=self.second_info, dont_filter= True, meta={'retry': retry, 'req_url': req_url})
            self.logger.error('TimeoutError on %s', request.url)
        else:
            pass

    def spider_idle(self):
        self.num_rest += 1
        if self.num_rest < 600:
            self.schedule_next_requests()
            raise DontCloseSpider
        else:
            print("spider closed !")
            raise CloseSpider