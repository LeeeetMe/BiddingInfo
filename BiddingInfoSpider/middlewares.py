# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import time
import requests
from selenium.webdriver.support import expected_conditions as EC

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BiddinginfospiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BiddinginfospiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self, timeout=None, proxy_list=None):
        self.timeout = timeout
        options = webdriver.ChromeOptions()
        options.add_argument('-headless')
        self.browser = webdriver.Chrome(options=options)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if request.meta.get("close"):
            spider.crawler.engine.close_spider(spider, "主动关闭爬虫:" + spider.name + "-" + spider.website_name)
        dynamic_flag = request.meta.get('dynamic', False)
        xpath = request.meta.get('xpath', False)
        if dynamic_flag:
            try:
                self.browser.get(request.url)
                if xpath:
                    self.wait.until(
                        EC.presence_of_element_located((By.XPATH, xpath)))
                else:
                    time.sleep(1)
                return HtmlResponse(url=request.url, body=self.browser.page_source, request=request,
                                    encoding='utf-8', status=200)
            except Exception as e:
                print('超过加载等待时间', e)
                return HtmlResponse(url=request.url, status=500, request=request)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HttpbinProxyMiddleware(object):
    def get_proxy(self):
        response = requests.get("http://192.168.1.56:8069/get")
        res = json.loads(response.text)
        if res.get("code") == 200:
            return res.get("proxy")
        else:
            return self.get_proxy()

    def process_request(self, request, spider):
        # TODO 无法获取https高匿代理IP，导致部分爬虫无法通过代理IP爬取
        print(request.url)
        request.meta['proxy'] = self.get_proxy()
