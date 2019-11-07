from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


# class SiChuan(BaseSpider):
#     name = 'SiChuan'
#     allowed_domains = ['ggzyjy.zgzhijiang.gov.cn']
#     start_urls = ['http://ggzyjy.sc.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData']
#     website_name = '宜昌市公共资源交易中心'
#     tmpl_url = "http://ggzyjy.sc.gov.cn/inteligentsearch/rest/inteligentSearch/getFullTextData"
#     category = "工程建设"
#
#     def __init__(self, *a, **kw):
#         super(SiChuan, self).__init__(*a, **kw)
#         if not self.biddingInfo_update:
#             pass
#
#     def start_requests(self):
#         form_data = {
#             "token": "",
#             "pn": "0",
#             "rn": "12",
#             "sdt": "",
#             "edt": "",
#             "wd": "",
#             "inc_wd": "",
#             "exc_wd": "",
#             "fields": "title",
#             "cnum": "",
#             "sort": "{'webdate':'0'}",
#             "ssort": "title",
#             "cl": "500",
#             "terminal": "",
#             "condition": '''[{
#                 "fieldName": "categorynum", "equal": "002",
#                 "notEqual": None, "equalList": None, "notEqualList": None,
#                 "isLike": True, "likeType": 2}]''',
#             "time": '''[{"fieldName": "webdate", "startTime": "2019-10-6 00:00:00", "endTime": "2019-11-6 23:59:59"}]''',
#             "highlights": "",
#             "statistics": "",
#             "unionCondition": "",
#             "accuracy": "",
#             "noParticiple": "0",
#             "searchRange": "",
#             "isBusiness": "1"}
#
#         yield scrapy.FormRequest(url=self.tmpl_url, dont_filter=True, callback=self.parse_item, formdata=form_data)
#
#     def parse_item(self, response):
#         item = response.meta["item"]
#
#         print(response.url)
#         article = response.xpath('//div[@id="mainContent"]//p')
#         # 去除句子中的\xa0\xa0，返回列表
#         content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
#         attachments = article.xpath(
#             './/a[contains(@href,".pdf") \
#             or contains(@href,".rar") \
#             or contains(@href,".doc") \
#             or contains(@href,".xls") \
#             or contains(@href,".zip") \
#             or contains(@href,".docx")]')
#         attachments_dict = self.get_attachment(attachments, response.request.url)
#         item.update(
#             content=content,
#             attachments=attachments_dict
#         )
#         print(item)
#         # yield item
