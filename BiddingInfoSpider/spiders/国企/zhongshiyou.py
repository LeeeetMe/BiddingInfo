import json

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from scrapy.selector import Selector


# class ZhongShiYou(BaseSpider):
#     name = 'ZhongShiYou'
#     allowed_domains = ['cnpcbidding.com']
#     start_urls = ['https://www.cnpcbidding.com/cms/pmsbidInfo/listPageOut']
#     website_name = '中国石油招标投标网'
#     tmpl_url = 'https://www.cnpcbidding.com/cms/pmsbidInfo/listPageOut'
#     endPageNum = 20
#     headers = {
#         "Content-Type": "application/json;charset=UTF-8",
#         "X-Requested-With": "XMLHttpRequest",
#         "Referer": "https://www.cnpcbidding.com/html/1/index.html",
#         # "Cookie": "JSESSIONID=EBAF2D721139BF6581C9F4FCA6BA5152"
#     }
#
#     def start_requests(self):
#         for i in range(1, self.endPageNum):
#             form_data = {
#                 "categoryId": "199",
#                 "pageNo": 3,
#                 "pageSize": 15,
#                 "pid": "198",
#                 "title": "",
#                 "url": "./list.html"
#             }
#             # payload
#             request = scrapy.Request(self.tmpl_url,
#                                      callback=self.parse_page,
#                                      headers=self.headers,
#                                      method="POST",
#                                      body=json.dumps(form_data),
#                                      dont_filter=True)
#             yield request
#
#     def parse_page(self, response):
#         print('request_url= ', response.request.url)
#         res = json.loads(str(response.body, encoding="utf-8"))
#         data_list = res['list']
#         if data_list:
#             tmp_href = 'https://www.cnpcbidding.com/cms/pmsbidInfo/detailsOut'
#             for data in data_list:
#                 item = dict()
#                 print(data)
#                 title = data.get("projectname")
#                 ctime = data.get("dateTime")
#                 id = data.get("id")
#                 code = data.get('projectcode')
#                 item.update(
#                     title=title,
#                     code=code,
#                     ctime=ctime,
#                 )
#                 form_data = {
#                     "url": "./page.html", "pid": "198", "pageSize": "",
#                     "categoryId": "199", "title": "", "pageNo": "", "dataId": id}
#
#                 # payload
#                 request = scrapy.Request(tmp_href,
#                                          callback=self.parse_item,
#                                          headers=self.headers,
#                                          method="POST",
#                                          body=json.dumps(form_data),
#                                          dont_filter=True,
#                                          meta={"item": item})
#                 yield request
#
#     def parse_item(self, response):
#         item = response.meta["item"]
#         res = json.loads(str(response.body, encoding="utf-8"))
#         attachment_tmp = 'https://www.cnpcbidding.com/pmsbid/download?id={0}&skip=true'
#         attachments_dict = dict()
#         att_list = res.get("attachmentList")
#         if att_list and isinstance(att_list, list):
#             for att in att_list:
#                 att_url = attachment_tmp.format(att.get("ATTACHMENTID"))
#                 att_name = att.get("NAME")
#                 attachments_dict.update({att_name: att_url})
#         article = res.get("list")[0]
#         content = []
#         if article:
#             item["code"] = article.get("projectcode")
#             content = Selector(text=article.get("bulletincontent"))
#             content = ["".join(i.split()) for i in content.xpath('normalize-space(string(.))').extract()]
#         item.update(
#             content=content,
#             attachments=attachments_dict,
#         )
#         print(item)
#         # yield item
