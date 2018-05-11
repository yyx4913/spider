# -*- encoding: utf-8 -*-
from scrapy.exceptions import DontCloseSpider, CloseSpider
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
import pymongo,random,time,json
from selenium import webdriver
from scrapy import Selector
import re
from spider_redis.items import CompanyDetailItem

# 模拟天眼查登陆获取数据
class TycinfoSpider(RedisSpider):
    name = 'tycinfo'
    allowed_domains = ['tianyancha.com']
    redis_key = 'tyc:start_urls'
    mongo = pymongo.MongoClient('IP', 27017).db.table  
    num_rest = 0
    username = '******'   # 用户名
    pwd = '********'  # 密码
    search_url = 'https://www.tianyancha.com/search?key='
    custom_settings = {
        'REDIS_PARAMS': {
            'password': '*****',
            'db': ****
        },
        'DOWNLOADER_MIDDLEWARES': {
            'spider_redis.middlewares.ProcessHeaderMidware': 111,
        },
        'ITEM_PIPELINES': {
            'spider_redis.pipelines.TycSeleniumPipeline': 300,
        },
        'RETRY_TIMES': 2,
        'DOWNLOAD_TIMEOUT': 15,
        'CONCURRENT_REQUESTS': '1',
        'CONCURRENT_REQUESTS_PER_IP': '1',
        # 'DOWNLOAD_DELAY': random.randint(5, 8),
        # 'LOG_FILE': './logs/tyc.log',
        # 'LOG_FORMAT': '%(name)s-%(levelname)s: %(message)s',
        # 'LOG_LEVEL': 'ERROR'
    }
    def __init__(self):

        self.driver = self.getDriver(self.username, self.pwd)

    def getDriver(self, username, pwd):
        chrome_opts = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2} # 设置不加载图片
        chrome_opts.add_experimental_option('prefs', prefs)
        chrome_opts.set_headless() # 设置无头浏览
        chrome_path = "/usr/local/bin/chromedriver" # chromedriver存放的位置
        driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_opts)
        driver.get('https://www.tianyancha.com/search')
        driver.implicitly_wait(10)
        time.sleep(2)
        driver.find_element_by_xpath('//div[@class="pb30 position-rel"]/input').send_keys(username)
        driver.find_element_by_xpath('//div[@class="pb40 position-rel"]/input').send_keys(pwd)
        driver.find_element_by_xpath('//div[@tyc-event-ch="Login.Login"]').click()
        time.sleep(2)
        return driver

    def parse(self, response):
        res = self.mongo.find().batch_size(100)
        for i in res:
            aim_id = i['_id']
            key = i['name']
            tag = 0
            time.sleep(random.randint(5,10))
            self.driver.find_element_by_xpath('//input[@id="header-company-search"]').clear()
            self.driver.find_element_by_xpath('//input[@id="header-company-search"]').send_keys(key)
            self.driver.find_element_by_xpath('//div[@tyc-event-ch="DaoHang.CompanySearch.Search"]').click()
            time.sleep(random.randint(5,10))
            sel = Selector(text=self.driver.page_source)
            divs = sel.xpath('//div[@class="b-c-white search_result_container"]/div')
            if not divs: # 出现验证码
                self.driver.quit() # 退出更换账号或者花钱找打码平台破解验证码就不用换账号
                self.driver = self.getDriver('username', 'password')
                time.sleep(random.randint(5, 20))
                self.driver.find_element_by_xpath('//input[@id="header-company-search"]').clear()
                self.driver.find_element_by_xpath('//input[@id="header-company-search"]').send_keys(key)
                self.driver.find_element_by_xpath('//div[@tyc-event-ch="DaoHang.CompanySearch.Search"]').click()
                time.sleep(random.randint(5, 20))
                sel = Selector(text=self.driver.page_source)
                divs = sel.xpath('//div[@class="b-c-white search_result_container"]/div')

            for div in divs:
                url = div.xpath('./div[2]/div/a/@href').extract_first()
                res = re.search(r'(\d+)',url)
                id = res.group(1) if res else ''
                if id and id == aim_id:
                    tag = 1
                    item = CompanyDetailItem()
                    item['name'] = key
                    item['url'] = url
                    item['legalPersonName'] = div.xpath('./div[@class="search_right_item ml10"]//a/@title').extract_first()
                    item['regCapital']= div.xpath('./div[@class="search_right_item ml10"]//div[@class="title overflow-width"][2]/span/text()').extract_first()
                    item['regTime']= div.xpath('./div[@class="search_right_item ml10"]//div[@class="title overflow-width"][3]/span/text()').extract_first()
                    item['phoneNumber']= div.xpath('./div//div[@class="add pb5"]/span[2]').extract_first()
                    self.driver.get(url=url)
                    time.sleep(random.randint(5, 10))
                    selector = Selector(text=self.driver.page_source)
                    item['email'] = selector.xpath(u'//span[text()="邮箱："]/following-sibling::span[1]/text()').extract_first()
                    item['websiteList'] = selector.xpath(u'//span[text()="网址："]/following-sibling::span[1]/text()').extract_first()
                    item['address'] = selector.xpath(u'//span[text()="地址："]/following-sibling::span[1]/text()').extract_first()
                    item['regAddress'] = selector.xpath(u'//td[text()="注册地址"]/following-sibling::td[1]/text()').extract_first()
                    item['regInstitute'] = selector.xpath(u'//td[text()="登记机关"]/following-sibling::td[1]/text()').extract_first()
                    item['orgNumber'] = selector.xpath(u'//td[text()="组织机构代码"]/following-sibling::td[1]/text()').extract_first()
                    item['regStatus'] = selector.xpath(u'//div[text()="公司状态"]/following-sibling::div[1]/div/@title').extract_first()
                    yield item
                else:
                    continue
            if not tag:
                self.logger.error('key %s, id %s has not found in first page', key, aim_id)


    def spider_idle(self):
        self.num_rest += 1
        if self.num_rest < 100:
            self.schedule_next_requests()
            raise DontCloseSpider
        else:
            print("spider is closed!")
            raise CloseSpider



