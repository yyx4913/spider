# -*- coding: utf-8 -*-

# Scrapy settings for spider_redis project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider_redis'

SPIDER_MODULES = ['spider_redis.spiders']
NEWSPIDER_MODULE = 'spider_redis.spiders'

# 确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 启动从reids缓存读取队列,调度爬虫
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 调度状态持久化，不清理redis缓存，允许暂停/启动爬虫
SCHEDULER_PERSIST = True

# 请求调度使用优先队列（默认)
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# 采用LIFI
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'
# 采用FIFI
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

REDIS_HOST = '*********'
REDIS_PORT = 6379

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'spider_redis (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 手机版user_agent
USER_AGENT_LIST = [
    "Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
    "Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
    "Mozilla/5.0 (iPhone 92; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.7.2 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
    "Mozilla/5.0 (iPhone 91; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14C92 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
    "Mozilla/5.0 (iPhone 6sp; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.8.0 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 search%2F1.0 baiduboxapp/0_0.1.1.7_enohpi_8022_2421/1.2.9_1C2%257enohPi/1099a/088D84D1E9A6AEE91798B97AAA03690B96CFCB638FGIMSINMHB/1",
    "Mozilla/5.0 (iPhone 6; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/6.0 MQQBrowser/6.6.1 Mobile/13E238 Safari/8536.25",
    "Mozilla/5.0 (iPhone 6p; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
    "Mozilla/5.0 (iPhone 6p; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 MQQBrowser/7.8.0 Mobile/12B436 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
    "Mozilla/5.0 (iPhone 6s; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 MQQBrowser/7.8.0 Mobile/13F69 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
    "Mozilla/5.0 (iPhone 6s; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/6.0 MQQBrowser/6.9 Mobile/14B100 Safari/8536.25 MttCustomUA/2",
    "Mozilla/5.0 (iPhone 92; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.2.1 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
    "Mozilla/5.0 (iPhone 92; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 MQQBrowser/7.8.0 Mobile/15A372 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OD105 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.4.950 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.8.945 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OD105 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.7.8.958 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.7 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OD105 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.5.955 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-cn; OD105 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM919 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.2.954 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; SM919 Build/MXB48T) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.0) WindVane/8.0.0 1440X2560 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; YQ601 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.4.3) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; SM801 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.5.3) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; SM801 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.0) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; SM919 Build/MXB48T) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.4.3) WindVane/8.0.0 1440X2560 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; SM919 Build/MXB48T) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.3.2) WindVane/8.0.0 1440X2560 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; Android 5.1.1; SM801 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043015 Safari/537.36 V1_AND_SQ_6.6.9_482_YYB_D QQ/6.6.9.3060 NetType/2G WebP/0.3.0 Pixel/1080",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; SM801 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.9.7.737 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; Android 5.1.1; SM801 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile MQQBrowser/6.8 TBS/036887 Safari/537.36 V1_AND_SQ_6.6.1_442_YYB_D QQ/6.6.1.2960 NetType/2G WebP/0.3.0 Pixel/1080",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; YQ601 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.9.3.727 U3/0.8.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; YQ601 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/6.8 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1; OPPO R9tm Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1)",
    "Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080",
    "Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/WIFI WebP/0.3.0 Pixel/720",
    "Mozilla/5.0 (Linux; Android 5.1; OPPO A37m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1)",
    "Mozilla/5.0 (Linux; Android 5.1; OPPO A59s Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1)",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OPPO R11 Pluskt Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36 ",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1)",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; OPPO A57 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 7.1.1)",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; R7Plusm Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; OPPO R9m Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; OPPO A59s Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.6.951 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; OPPO R9s Plus Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; OPPO R9m Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.7 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 4.4.4; R7c Build/KTU84P; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/7.9 baiduboxapp/9.0.0.10 (Baidu; P1 4.4.4)",
    "Mozilla/5.0 (Linux; Android 4.4.4; 3007 Build/KTU84P; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/7.9 baiduboxapp/9.0.0.10 (Baidu; P1 4.4.4)",
    "Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/7.9 baiduboxapp/9.0.0.10 (Baidu; P1 5.1)",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; OPPO R9 Plustm A Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.1 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; OPPO R9m Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.1.949 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1.1; OPPO R11 Plus Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043305 Safari/537.36 V1_AND_SQ_7.1.5_708_YYB_D QQ/7.1.5.3215 NetType/WIFI WebP/0.3.0 Pixel/720",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.26 Mobile Safari/537.36 AliApp(TB/7.1.6) WindVane/8.0.0 1080X1920",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; OPPO R11t Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.2) WindVane/8.3.0 1080X1920",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; OPPO R9sk Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.3) WindVane/8.3.0 1080X1920",
    "Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; OPPO R9tm Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.3) WindVane/8.3.0 1080X1920",
    "Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; OPPO A59s Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.3) WindVane/8.3.0 720X1280",
    "Mozilla/5.0 (Linux; Android 5.0.2; vivo X6A Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.0.2)",
    "Mozilla/5.0 (Linux; Android 5.1; vivo X6Plus D Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080",
    "Mozilla/5.0 (Linux; Android 6.0; vivo Y67A Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.4 baiduboxapp/8.5 (Baidu; P1 6.0)",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; vivo Y66L Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.7 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; vivo Y67 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.2 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.0.2; vivo X6A Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 5.0.2)",
    "Mozilla/5.0 (Linux; Android 5.1.1; vivo Y51A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 5.1.1)",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.0.2; vivo Y51A Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.1 baiduboxapp/9.1.5.10 (Baidu; P1 5.0.2)",
    "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6SPlus A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/7.9 baiduboxapp/9.0.0.10 (Baidu; P1 5.1.1)",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; vivo Y51A Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; vivo X9s L Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 7.1.1)",
    "Mozilla/5.0 (Linux; Android 5.1; vivo X6Plus D Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 5.1)",
    "Mozilla/5.0 (Linux; Android 7.1.1; vivo X9i Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 7.1.1)",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; vivo Y66 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.7 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; vivo V3 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.7 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.0.2; vivo Y37 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/7.9 baiduboxapp/9.0.0.10 (Baidu; P1 5.0.2)",
    "Mozilla/5.0 (Linux; Android 5.0.2; vivo Y937 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/7.9 baiduboxapp/9.0.0.10 (Baidu; P1 5.0.2)",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; vivo X9Plus Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.1.949 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; vivo X9 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.1.939 UCBS/2.10.1.8 Mobile Safari/537.36 AliApp(TB/6.9.1) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
    "Mozilla/5.0 (Linux; Android 5.1.1; vivo V3Max A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 5.1.1)",
    "Mozilla/5.0 (Linux; Android 5.1.1; vivo Xplay5A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 5.1.1)",
    "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-CN; vivo X6Plus A Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.3) WindVane/8.3.0 1080X1920",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; vivo X20Plus A Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.3) WindVane/8.3.0 1080X2040",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3",
    "Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; MI 5X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.2.2",
    "Mozilla/5.0 (Linux; Android 7.0; MIX Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/WIFI WebP/0.3.0 Pixel/1080",
    "Mozilla/5.0 (Linux; Android 6.0.1; MI 4LTE Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.1.5_708_YYB_D QQ/7.1.5.3215 NetType/4G WebP/0.3.0 Pixel/1080",
    "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 Maxthon/3047",
    "Mozilla/5.0 (Linux; Android 6.0.1; MI 5s Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/WIFI WebP/0.3.0 Pixel/1080",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI 4LTE Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.2.2",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-cn; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.6 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI 5s Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.9.5",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.7.7",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.9.6",
    "Mozilla/5.0 (Linux; Android 7.0; MI MAX Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043307 Safari/537.36 MicroMessenger/6.5.10.1080 NetType/WIFI Language/zh_CN	",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-cn; Mi Note 3 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/8.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.2) WindVane/8.3.0 1080X1920",
    "Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; MI 5X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/8.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI NOTE Pro Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.3.10",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; Mi Note 2 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/8.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.8.1.961 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-cn; MIX 2 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/8.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-cn; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.3.10 tae_sdk_a_2.1.0 AliApp(BC/2.1.0)",
    "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-CN; MI 2S Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.8.0.960 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; MI MAX Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.2.4) WindVane/8.3.0 1080X1920",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-cn; Mi Note 3 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.3.10",
    "Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; Mi Note 3 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.2.4) WindVane/8.3.0 1080X1920",
    "Mozilla/5.0 (Linux; Android 7.0; MI 5s Plus Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/10.0 baiduboxapp/10.0.5.11 (Baidu; P1 7.0)",
    "Mozilla/5.0 (Linux; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.1.0_0_TIM_D TIM2.0/1.2.0.1692 QQ/6.5.5 NetType/2G WebP/0.3.0 Pixel/1080 IMEI/869953022249635",
    "Mozilla/5.0 (Linux; Android 6.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.3 baiduboxapp/9.3.0.10 (Baidu; P1 6.0)",
    "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; EVA-DL00 Build/HUAWEIEVA-DL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; PLK-AL10 Build/HONORPLK-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; HUAWEI CAZ-TL10 Build/HUAWEICAZ-TL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.4 baiduboxapp/8.3.1 (Baidu; P1 6.0)",
    "Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; HUAWEI TAG-TL00 Build/HUAWEITAG-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.8.952 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1; HUAWEI TIT-TL00 Build/HUAWEITIT-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 5.1)",
    "Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; HUAWEI NXT-TL00 Build/HUAWEINXT-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.4.950 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; FRD-AL10 Build/HUAWEIFRD-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.1 baidubrowser/7.15.15.0 (Baidu; P1 7.0)",
    "Mozilla/5.0 (Linux; Android 5.1; HUAWEI TIT-AL00 Build/HUAWEITIT-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 5.1)",
    "Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-CL00 Build/HUAWEINXT-CL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/7.9 baiduboxapp/9.0.0.10 (Baidu; P1 7.0)",
    "Mozilla/5.0 (Linux; Android 7.0; EVA-AL10 Build/HUAWEIEVA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 7.0)",
    "Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-CL00 Build/HUAWEINXT-CL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 7.0)",
    "Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.2 baiduboxapp/9.2.0.10 (Baidu; P1 7.0)",
    "Mozilla/5.0 (Linux; U; Android 5.0.1; zh-cn; HUAWEI GRA-TL00 Build/HUAWEIGRA-TL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/31.0.0.0 MQQBrowser/7.5 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; H60-L12 Build/HDH60-L12) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/23.0.1654.15 UCBrowser/9.2.1.416 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 6.0; zh-cn; HUAWEI GRA-TL00 Build/HUAWEIGRA-TL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.7 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 rabbit/1.0 baiduboxapp/7.1 (Baidu; P1 7.0)",
    "Mozilla/5.0 (Linux; U; Android 5.0.1; zh-cn; HUAWEI GRA-TL00 Build/HUAWEIGRA-TL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.3 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; FRD-AL00 Build/HUAWEIFRD-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.7 Mobile Safari/537.36",
]

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# RETRY_HTTP_CODES
HTTP_ALLOWED_CODES = [503, 504, 505 ]
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 429, 403, 302]
# Disable cookies (enabled by default)
# COOKIES_ENABLED = False
# REDIRECT_ENABLED = False
# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'spider_redis.middlewares.ZebraSpiderRedisSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'spider_redis.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
