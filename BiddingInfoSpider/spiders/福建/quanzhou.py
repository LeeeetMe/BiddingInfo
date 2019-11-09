import json
import random

import requests

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


# class QuanZhou(BaseSpider):
#     name = 'QuanZhou'
#     allowed_domains = ['lyszb.com']
#     start_urls = ['http://ggzyjy.quanzhou.gov.cn/project/getProjPage_project.do']
#     website_name = '泉州市公共资源交易信息网'
#     tmpl_url = 'http://ggzyjy.quanzhou.gov.cn/project/getProjPage_project.do'
#     category = "工程建设"
#     endPageNum = 2
#     headers = {
#         # "Host": "www.lyszb.com",
#         # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
#         # "Accept": "application/json, text/javascript, */*; q=0.01",
#         # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
#         # "Accept-Encoding": " gzip, deflate",
#         "Content-Type": "application/json;charset=UTF-8",
#         "X-Requested-With": "XMLHttpRequest",
#         "Origin": "http://ggzyjy.quanzhou.gov.cn",
#         # "Connection": "keep-alive",
#         "Referer": "http://ggzyjy.quanzhou.gov.cn/project/projectList.do?centerId=-1"
#     }
#
#     def start_requests(self):
#         for i in range(1, self.endPageNum):
#             form_data = {"pageIndex": str(i), "pageSize": "10", "classId": "0", "centerId": "0", "projNo": "",
#                          "projName": "", "ownerDeptName": ""}
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
#         data_list = res["data"]["dataList"]
#         if data_list:
#             tmp_href = 'http://ggzyjy.quanzhou.gov.cn/project/projectInfo.do?projId={0}'
#             article_url = 'http://ggzyjy.quanzhou.gov.cn/project/getProjDetail_project.do'
#             file_url = 'http://ggzyjy.quanzhou.gov.cn/project/getProjAttachList_project.do'
#             for data in data_list:
#                 item = dict()
#                 title = data.get("projName")
#                 code = data.get("projNo")
#                 ctime = data.get("auditDate")
#                 tenderProjId = data.get("tradeProjId")
#                 href = tmp_href.format(tenderProjId)
#                 artcileData = {
#                     "projId": str(tenderProjId)
#                 }
#                 attachmentData = {
#                     "projId": str(tenderProjId),
#                     "fileType": "F001"
#                 }
#                 article = json.loads(
#                     requests.post(article_url, data=json.dumps(artcileData), headers=self.headers).text)
#                 attachments = json.loads(
#                     requests.post(file_url, data=json.dumps(attachmentData), headers=self.headers).text)
#                 attachments_dict = dict()
#                 content = list()
#                 if article:
#                     d = article.get("data")
#                     if d:
#                         content = [
#                             "招投标项目编号：" + d.get("projNo"),
#                             "招投标项目名称：" + d.get("projName"),
#                             "计划开工日期：" + d.get("planBgDate"),
#                             "计划竣工日期：" + d.get("planEdDate"),
#                             "招标人：" + d.get("ownerdeptname"),
#                             "招标代理：" + d.get("agentDept"),
#                             "造价咨询机构：" + d.get("projName"),
#                             "建设地点：" + d.get("buildArea"),
#                             "资金来源：" + d.get("fundSource"),
#                             "本次招标估算价(万元)" + str(d.get("totalInvest"))]
#
#                 if attachments:
#                     d = article.get("data")
#                     if d:
#                         attachments_dict.update(
#                             {d.get("fileTitle") or str(random.randint(1, 100)): d.get("downPath")}
#                         )
#                 item.update(
#                     category=self.category,
#                     title=title,
#                     code=code,
#                     ctime=ctime,
#                     href=href,
#                     content=content,
#                     attachments=attachments_dict,
#                     city="泉州",
#                 )
#                 # print(item)
#                 yield item
