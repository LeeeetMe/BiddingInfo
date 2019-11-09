import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
from selenium import webdriver
import requests


class GanShu(BaseSpider):
    name = 'ganshu'
    allowed_domains = ['ggzyjy.gansu.gov.cn']
    start_urls = ['http://ggzyjy.gansu.gov.cn/f/newprovince/annogoods/list']
    website_name = '甘肃省公共资源交易'
    tmpl_url = 'http://ggzyjy.gansu.gov.cn/f/newprovince/annogoods/getAnnoList'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(GanShu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 50

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {"pageNo": str(i), "pageSize": "10", "area": "620000", "projecttype": "A",
                         "prjpropertynewI": "I",
                         "prjpropertynewA": "A", "prjpropertynewD": "D", "prjpropertynewC": "C", "prjpropertynewB": "B",
                         "prjpropertynewE": "E", "projectname": ""}

            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True, )
            yield request

    def parse_page(self, response):
        a = response.xpath('//div[@class="sTradingInformationSelectedBtoList"]//a')

        for a1 in a:
            item = BiddinginfospiderItem()
            item['href'] = response.urljoin(a1.xpath('.//@href').extract_first())
            item['title'] = a1.xpath(".//text()").extract_first().strip()
            item['ctime'] = a1.xpath('..//..//i//text()').extract_first()
            item['city'] = '甘肃省'

            data = {"bidpackages": "", "tenderprojectid": item['href'].split('/')[-2], "index": "0"}

            # yield scrapy.Request(url=item['href'], dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            # request = FormRequest('http://ggzyjy.gansu.gov.cn/f/newprovince/tenderproject/flowpage',
            #                       callback=self.parse_item, formdata=data, dont_filter=True, meta={'meta': item, })
            # yield request
            yield item

    def parse_item(self, response):
        # options = webdriver.ChromeOptions()
        # options.add_argument('-headless')
        # driver = webdriver.Chrome(options=options)
        # driver.get(response.request.url)
        # driver.implicitly_wait(5)
        # html = driver.page_source
        # a = driver.find_element_by_xpath('//div[@class="jxTradingPublic"]')

        item = response.meta['meta']
        # 主体
        main = response.xpath('//div[@class="jxTenderObjMain"]')
        # 正文
        item['content'] = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]

        html = requests.get(item['href'], ).text
        selector = Selector(text=html)
        no = selector.xpath('//li[@class="jxTradingBianma"]//text()').extract_first().strip().split('-')[0][5:]
        data2 = {"tenderprojectid": str(item['href'].split('/')[-2]), "bidpackages": "", "projectType": str(no)}

        html2 = requests.post('http://ggzyjy.gansu.gov.cn/f/newprovince/tenderproject/flowBidpackage', data=data2).text
        selector2 = Selector(text=html2)
        content2 = selector2.xpath('//div[@class="sAblock"]')
        content3 = ["".join(i.split()) for i in content2.xpath('normalize-space(string(.))').extract()]
        item['content'] += content3

        # 附件
        attach = main.xpath(
            './/a[contains(text(),".pdf") or contains(text(),".rar") or contains(text(),".doc") or contains(text(),".xls") or contains(text(),".zip") or contains(text(),".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments

        print(item)


