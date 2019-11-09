import json
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class AnHui(BaseSpider):
    name = 'anhui'
    allowed_domains = ['ggzy.ah.gov.cn']
    start_urls = ['http://ggzy.ah.gov.cn/bulletininfo.do?method=showList&fileType=1&hySort=&bulletinclass=jy&num=1']
    website_name = '安徽公共资源交易'
    tmpl_url = 'http://ggzy.ah.gov.cn/dwr/call/plaincall/bulletinInfoDWR.getPackListForDwr1.dwr'
    pageIndex = 1

    def __init__(self, *a, **kw):
        super(AnHui, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 2

    def start_requests(self):
        headers = {
            'Accept':'*/*',
            "Content-Type": "text/plain",
            "Content-Length":"807",
            "Host": "ggzy.ah.gov.cn",
            "Origin": "http://ggzy.ah.gov.cn",
            "Referer": "http://ggzy.ah.gov.cn/bulletininfo.do?method=showList&fileType=1&hySort=&bulletinclass=jy&num=1",
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            # 'Cookie':'JSESSIONID=8432a9303336f8ff0958688a3868;_gscu_118004476=73170700tifdmw88;_gscs_118004476=73170700cjlbkm88|pv:1;_gscbrs_118004476=1'
        }
        for i in range(1, self.pageIndex):
            form_data = 'callCount=1&page=/bulletininfo.do?method=showList&fileType=1&hySort=&bulletinclass=jy&num=1&&httpSessionId=8432a9303336f8ff0958688a3868&scriptSessionId=2CDBFC31AAD9855F56DA5CF2CBF0338D670&c0-scriptName=bulletinInfoDWR&c0-methodName=getPackListForDwr1&c0-id=0&c0-e1=string:2&c0-e2=string:&c0-e3=string:jy&c0-e4=string:2&c0-e5=string:&c0-e6=string:&c0-e7=string:&c0-e8=number:2&c0-e9=string:10&c0-e10=string:true&c0-e11=string:packTable&c0-e12=string:44677&c0-param0=Object_Object:{id:reference:c0-e1,hySort:reference:c0-e2,bulletinclass:reference:c0-e3,fileType:reference:c0-e4,bulletinType:reference:c0-e5,district:reference:c0-e6,srcdistrict:reference:c0-e7,currentPage:reference:c0-e8,pageSize:reference:c0-e9,isPage:reference:c0-e10,tabId:reference:c0-e11,totalRows:reference:c0-e12}&batchId=2'
            yield scrapy.Request(url=self.tmpl_url, dont_filter=True, callback=self.parse_page, method='POST',
                                 headers=headers,
                                 body=form_data,
                                 meta={"dynamic": True,})
            # request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True,)
            # yield request

    def parse_page(self, response):
        rs = response.body.decode('utf8')
        print('#######', rs)
        return
