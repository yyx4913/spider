# -*- coding: utf-8 -*-
from scrapy.exceptions import DontCloseSpider, CloseSpider
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from datetime import datetime
from scrapy.utils.project import get_project_settings
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError, DNSLookupError
import json
from spider_redis.items import LibsPoiItem
import sys

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


# 高德周边搜POI
class LibsPoiSpider(RedisSpider):
    name = 'libs_poi_spider'
    redis_key = 'libs_poi:start_urls'
    settings = get_project_settings()
    num_rest = 0
    # ip_blackset = settings.get('IP_BLACKSET')
    custom_settings = {
        'REDIS_PARAMS': {
            'password': '****',
            'db': ***
        },
        'ITEM_PIPELINES': {
            'spider_redis.pipelines.LibsPoiPipeline': 300,
        },
        'LOG_FILE': './logs/libs_poi.logs',
        'LOG_FORMAT': '%(name)s-%(levelname)s: %(message)s',
        'LOG_LEVEL': 'ERROR',
        'REDIRECT_ENABLED': False,
        'RETRY_TIMES': 2,
        'DOWNLOAD_TIMEOUT': 40,
        # 'DOWNLOAD_DELAY': '0.05',
        'CONCURRENT_REQUESTS': '64',
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': '1'
    }

    def parse(self, response):
        self.num_rest = 0
        retry_time = response.meta['retry_time'] if 'retry_time' in response.meta else 0
        jo = json.loads(response.body)
        if jo.get('status') != '1':
            print('%s had show verification code!!! code ', response.url, response.status)
            if retry_time < 5:
                retry_time += 1
                yield Request(url=response.url,
                              callback=self.parse,
                              errback=self.log_error,
                              meta={'retry_times': retry_time},
                              dont_filter=True)
        elif 'pois' in jo.keys() and jo.get('pois'):
            pois = jo.get('pois')
            page_num = response.meta['page_num'] if 'page_num' in response.meta else 2
            home_url = response.url.split('&page')[0] if 'page' in response.url else response.url
            for poi in pois:
                item = LibsPoiItem()
                item['lid'] = poi.get('id', '')
                item['name'] = poi.get('name', '')
                item['tag'] = poi.get('tag').replace(',', '&').replace('，', '&').replace('\n','') if poi.get('tag','') else ''
                item['ltype'] = poi.get('type', '')
                item['typecode'] = poi.get('typecode', '')
                item['biz_type'] = poi.get('biz_type') if poi.get('biz_type', '') else ''
                item['address'] = poi.get('address').replace(',', '&').replace('，', '&').replace('\n','') if poi.get('address','') else ''
                location = poi.get('location').split(',') if poi.get('location','') else ''
                if len(location) ==2:
                    item['lng'] = location[0]
                    item['lat'] = location[1]
                item['tel'] = poi.get('tel') if poi.get('tel', '') else ''
                item['postcode'] = poi.get('postcode') if poi.get('postcode', '') else ''
                item['website'] = poi.get('website') if poi.get('website', '') else ''
                item['email'] = poi.get('email') if poi.get('email', '') else ''
                item['pcode'] = poi.get('pcode') if poi.get('pcode', '') else ''
                item['pname'] = poi.get('pname') if poi.get('pname','') else ''
                item['citycode'] = poi.get('citycode')
                item['cityname'] = poi.get('cityname')
                item['adcode'] = poi.get('adcode') if poi.get('adcode','') else ''
                item['adname'] = poi.get('adname') if poi.get('adname','') else ''
                item['importance'] = poi.get('importance') if poi.get('importance', '') else ''
                item['shopid'] = poi.get('shopid') if poi.get('shopid', '') else ''
                item['shopinfo'] = poi.get('shopinfo') if poi.get('shopinfo','') else ''
                item['poiweight'] = poi.get('poiweight') if poi.get('poiweight', '') else ''
                item['gridcode'] = poi.get('gridcode') if poi.get('gridcode', '') else ''
                item['distance'] = poi.get('distance') if poi.get('distance', '') else ''
                item['navi_poiid'] = poi.get('navi_poiid') if poi.get('navi_poiid', '') else ''
                entr_location = poi.get('entr_location').split(',') if poi.get('entr_location', '') else ''
                if len(entr_location) == 2:
                    item['entr_lng'] = entr_location[0]
                    item['entr_lat'] = entr_location[1]
                item['business_area'] = poi.get('business_area') if poi.get('business_area', '') else ''
                item['exit_location'] = poi.get('exit_location').replace(',', '&') if poi.get('exit_location', '') else ''
                item['match'] = poi.get('match') if poi.get('match', '') else ''
                item['recommend'] = poi.get('recommend') if poi.get('recommend', '') else ''
                item['timestamp'] = poi.get('timestamp') if poi.get('timestamp', '') else ''
                item['alias'] = poi.get('alias', '') if poi.get('alias', '') else ''
                item['indoor_map'] = poi.get('indoor_map', '')
                cpid = poi.get('indoor_data').get('cpid','') if poi.get('indoor_data', '') else ''
                item['cpid'] = cpid if cpid else ''
                floor = poi.get('indoor_data', '').get('floor','') if poi.get('indoor_data', '') else ''
                item['floor'] = floor if floor else ''
                truefloor = poi.get('indoor_data', '').get('truefloor','') if poi.get('indoor_data', '') else ''
                item['truefloor'] = truefloor if truefloor else ''
                # cmsid = poi.get('indoor_data').get('cmsid','') if poi.get('indoor_data', '') else ''
                # item['cmsid'] = cmsid if cmsid else ''
                item['groupbuy_num'] = poi.get('groupbuy_num', '')
                item['discount_num'] = poi.get('discount_num', '')
                rating = poi.get('biz_ext', '').get('rating','') if poi.get('biz_ext', '') else ''
                item['rating'] = rating if rating else ''
                cost = poi.get('biz_ext', '').get('cost', '') if poi.get('biz_ext', '') else ''
                item['cost'] = cost if cost else ''
                # item['meal_ordering'] = poi.get('biz_ext', '').get('meal_ordering') if poi.get('biz_ext', '') else ''
                item['event'] = poi.get('event') if poi.get('event', '') else ''
                item['children'] = poi.get('children', '') if poi.get('children', '') else ''
                # item['url'] = response.url
                yield item

            if len(pois) == 25:  # 翻页
                next_url = home_url + '&page=' + str(page_num)
                page_num +=1
                yield Request(url=next_url, callback=self.parse, errback=self.log_error,dont_filter=True,
                              meta={'retry_times': 0, 'page_num':page_num})
        else:
            self.logger.error('url %s has no pois', response.url)

    def log_error(self, failure):
        self.num_rest = 0
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s,datetime: %s', response.url, datetime.now())
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.requet
            self.logger.error('TimeoutError on %s,datetime: %s', request.url, datetime.now())
        else:
            pass

    def spider_idle(self):
        self.num_rest += 1
        if self.num_rest < 1800:
            self.schedule_next_requests()
            raise DontCloseSpider
        else:
            print("spider is closed!")
            raise CloseSpider
