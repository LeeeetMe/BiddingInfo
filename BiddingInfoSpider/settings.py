# -*- coding: utf-8 -*-

# Scrapy settings for BiddingInfoSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BiddingInfoSpider'

SPIDER_MODULES = ['BiddingInfoSpider.spiders']
NEWSPIDER_MODULE = 'BiddingInfoSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'BiddingInfoSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#     'BiddingInfoSpider.middlewares.BiddinginfospiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'BiddingInfoSpider.middlewares.BiddinginfospiderDownloaderMiddleware': 543,
    'BiddingInfoSpider.middlewares.HttpbinProxyMiddleware': 530,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'BiddingInfoSpider.pipelines.BiddinginfospiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 自定义配置，如果为真则执行增量爬取，为假则爬取所有列表。增量规则由spider实现
BIDDING_INFO_UPDATE = False

HTTPERROR_ALLOWED_CODES = [403, 405]

SELENIUM_TIMEOUT = 5

RANDOMIZE_DOWNLOAD_DELAY = True

FEED_URI = 'export_data/%(website_name)s-%(time)s.xls'
FEED_FORMAT = 'excel'
FEED_EXPORT_ENCODING = 'utf8'
FEED_EXPORT_FIELDS = ["web_site", "city", "category", "industry", "code", "title", "ctime", "href"]
FEED_EXPORTERS = {'excel': 'BiddingInfoSpider.excel.ExcelItemExporter'}
ITEM_DICT = {'title': '标题', 'ctime': '时间', 'web_site': '网站', 'href': '网址', "category": "种类",
             "code": "编号", "city": "城市", "industry": "行业"}
FIELDS = [ITEM_DICT[i] for i in FEED_EXPORT_FIELDS]

COMMANDS_MODULE = 'BiddingInfoSpider.commands'
