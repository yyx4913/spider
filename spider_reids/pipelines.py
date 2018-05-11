# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from spider_redis.items import NewHouseItem, ResoldHouseItem,WuBaDetailItem,RentHouseItem, CarHomeItem, CarFourItem, LibsPoiItem
import time,pymongo,redis
from spider_redis.send_email import send_mail
from pybloom import ScalableBloomFilter  # 布隆过滤器


class SpiderRedisPipeline(object):
    def process_item(self, item, spider):
        return item


# 二手房信息保存为csv
class ResoldHousePipeline(object):
    def __init__(self):
        self.files = {}
        self.file_path = './data/resold.%d.csv' % int(time.time())
        self.num = 0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['city_name', 'house_title', 'house_address', 'avg_price',
                                 'chain_month', 'resold_number', 'building_years', 'developers',
                                 'property_company', 'parking_number', 'plot_ratio', 'greening_rate', 'property_price',
                                 'property_type', 'total_area', 'total_houses', 'house_url',
                                 'map_lng', 'map_lat']}

        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        send_mail("%s is closed!,time is  %s" % (spider.name, time.ctime()))

    def process_item(self, item, spider):
        if isinstance(item, ResoldHouseItem):
            self.exporter.export_item(item)
            self.num += 1
        if self.num % 100 == 0:
            print("save resold_data %s times" % self.num)
        return item


# 新房信息保存为csv
class NewHousePipeline(object):
    def __init__(self):
        self.files = {}
        self.file_path = './data/new.%d.csv' % int(time.time())
        # self.file_path = '/root/house_price/new.csv'
        self.num = 0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['city_name', 'house_title', 'house_address', 'property_type', 'feature', 'total_price',
                                 'reference_price', 'sales_telephone', 'developers', 'min_payment', 'sales_date',
                                 'completion_date', 'sales_address', 'building_type', 'planning_number',
                                 'property_years', 'plot_ratio', 'greening_rate', 'progress_works', 'property_price',
                                 'property_company', 'parking_number', 'parking_rate', 'house_url', 'map_lng',
                                 'map_lat']}

        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        print("spider closed!")
        send_mail("%s is closed!,time is  %s" % (spider.name, time.ctime()))

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.exporter.export_item(item)
            self.num += 1
        if self.num % 100 == 0:
            print("save new_data %s times" % self.num)
        return item


# 城市均价信息保存为csv
class CityAvgPricePipeline(object):
    def __init__(self):
        self.files = {}
        self.file_path = './data/avg.csv'
        self.num = 0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['city_name', 'avg_price', 'last_price']}
        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        send_mail("%s is closed!,time is  %s" % (spider.name, time.ctime()))

        print("spider closed!")

    def process_item(self, item, spider):
        if isinstance(item, CityAvgItem):
            self.exporter.export_item(item)
            self.num += 1
        if self.num % 100 == 0:
            print("save avg_data %s times" % self.num)
        return item

# 天眼查公司详情页信息保存
class TycSeleniumPipeline(object):
    def __init__(self):
        self.files = {}
        self.file_path = './data/Tyc_Detail.%d.csv' % int(time.time())
        self.num = 1

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['name', 'legalPersonName', 'regCapital', 'regTime', 'phoneNumber', 'email', 'address',
                                 'regAddress', 'regInstitute', 'orgNumber', 'regStatus', 'websiteList', 'url'
                                 ]}
        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        print("spider closed!")
        send_mail("%s is closed!,time is  %s" % (spider.name, time.ctime()))

    def process_item(self, item, spider):
        if isinstance(item, CompanyDetailItem):
            self.exporter.export_item(item)
        return item

# 58公司信息保存
class WuBaPipeline(object):
    def __init__(self):
        self.files = {}
        self.file_path = './data/WuBa_Detail.%d.csv' % int(time.time())

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['shop_name', 'cate', 'tag_flag', 'city', 'hot_num', 'active_num', 'service_grade',
                                 'address', 'map_lat', 'map_lng', 'shop_url']}
        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        print("spider closed!")
        send_mail("%s is closed!,time is  %s" % (spider.name, time.ctime()))

    def process_item(self, item, spider):
        if isinstance(item, WuBaDetailItem):
            self.exporter.export_item(item)
        return item

# Cer_info公司信息保存
class CerPipeline(object):
    def __init__(self):
        self.files = {}
        self.mongo = pymongo.MongoClient('IP', 27017).****
        self.file_path = './data/cer_info.%d.csv' % int(time.time())

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['shop_name', 'cate', 'tag_flag', 'city', 'hot_num', 'active_num', 'service_grade',
                                 'address', 'map_lat', 'map_lng', 'shop_url']}
        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        print("spider closed!")
        send_mail("%s is closed!,time is  %s" % (spider.name, time.ctime()))

    def process_item(self, item, spider):
        if isinstance(item, WuBaDetailItem):
            self.mongo.insert_one({'_id': item['shop_url']})
            self.exporter.export_item(item)
        return item

# 58同城出租房信息保存
class WubaHousesPipeline(object):
    def __init__(self):
        self.files = {}
        self.file_path = './data/WubaHouses.%d.csv' % int(time.time())
        self.num = 1

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['city_name','price', 'domain', 'kind','type','year','built','z_area','car','gs','kf','address',
                                 'people','wuye','rj','lh','b_area','s_house','r_house', 'life','edu','house_title',
                                 'house_address', 'house_price', 'rent_way','house_kind','house_floor', 'detail_address',
                                 'map_lat', 'map_lng','url']}

        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        print("spider closed!")
        send_mail("%s is closed!,time is  %s" % (spider.name, time.ctime()))

    def process_item(self, item, spider):
        if isinstance(item, RentHouseItem):
            self.exporter.export_item(item)
            self.num += 1
        if self.num % 10 == 0:
            print("save data %s times" % self.num)
        return item

#  汽车之家
class CarHomePipeline(object):
    def __init__(self):
        self.files = {}
        self.file_path = './data/Carhome_info.%d.csv' % int(time.time())

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['brand', 'vender', 'kind', 'level', 'structure', 'engine', 'box',
                                 'guide_price', 'score', 'car_type', 'g_price', 'refer_price', 'status', 'url']}
        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        print("spider closed!")

    def process_item(self, item, spider):
        if isinstance(item, CarHomeItem):
            self.exporter.export_item(item)
        return item

#  汽车之家 4s店
class CarFourPipeline(object):
    def __init__(self):
        self.files = {}
        self.file_path = './data/CarFour_info.%d.csv' % int(time.time())

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['city', 'shop_name', 'level', 'brand', 'car_num', 'address', 'phone',
                                 'lat', 'lng', 'main_brand', 'url']}
        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        print("spider closed!")

    def process_item(self, item, spider):
        if isinstance(item, CarFourItem):
            self.exporter.export_item(item)
        return item

# 高德周边搜
class LibsPoiPipeline(object):
    filter_prefix = 'POI_'
    def __init__(self):
        self.files = {}
        self.file_path = './data/libs_poi.%d.csv' % int(time.time())
        self.filter = ScalableBloomFilter(initial_capacity=1024, error_rate=0.001,
                                          mode=ScalableBloomFilter.SMALL_SET_GROWTH)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(self.file_path, 'a+b')
        self.files[spider] = file
        kwargs = {
            'fields_to_export': ['lid','name','tag','ltype','typecode','biz_type','address','lng','lat','tel','postcode',
                                 'website','email','pcode','pname','citycode', 'cityname', 'adcode','adname','importance',
                                 'shopid','shopinfo','poiweight','gridcode','distance','navi_poiid','entr_lng','entr_lat','business_area',
                                 'exit_location','match','recommend','timestamp','alias','indoor_map','cpid','floor','truefloor',
                                 'groupbuy_num','discount_num','rating','cost','event','children']}
        self.exporter = CsvItemExporter(file, include_headers_line=False, **kwargs)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        print("spider closed!")

    def process_item(self, item, spider):
        if isinstance(item, LibsPoiItem):
            if self.filter_prefix + item.get('lid') in self.filter:
                return
            self.exporter.export_item(item)
            self.filter.add(self.filter_prefix + item.get('lid'))
        return item
