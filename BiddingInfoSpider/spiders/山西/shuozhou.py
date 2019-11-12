from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest
import json


class ShuoZhou(BaseSpider):
    name = 'ShuoZhou'
    allowed_domains = ['ggzyjy.zgzhijiang.gov.cn']
    start_urls = [
        'http://szggzy.shuozhou.gov.cn/moreInfoController.do?getMoreNoticeInfo&page=1&rows=10&dateFlag=3month&tableName=&projectRegion=&projectName=&beginReceivetime=&endReceivetime=']
    website_name = '全国公共资源交易平台(山西省•朔州市)'
    tmpl_url = "http://szggzy.shuozhou.gov.cn/moreInfoController.do?getMoreNoticeInfo&page=1&rows=1000&dateFlag=3month&tableName=&projectRegion=&projectName=&beginReceivetime=&endReceivetime="
    city = "山西省"
    category_dict = {
        'gcjs_notice': "工程建设",
        'zfcg_notice': "政府采购",
        'td_notice': "土地使用权",
        'ky_notice': "矿业权出让",
        'gycqsw_notice': "国有产权（实物）",
        'gycqgq_notice': "国有产权（股权）",
    }

    def __init__(self, *a, **kw):
        super(ShuoZhou, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = [self.tmpl_url]

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        body = json.loads(str(response.body, "utf-8"))
        li = body.get("obj")
        print(len(li))
        for l in li:
            item = BiddinginfospiderItem()
            title = l.get("PROJECTNAME")
            ctime = l.get("RECEIVETIME")
            category = l.get("TABLENAME")
            code = l.get("PROJECTCODE")
            url = l.get("URL", "") + "&id="
            id = l.get("ID", "")

            href = response.urljoin("?getNoticeDetail&url=" + url + id)

            print(href)
            item.update(
                category=self.category_dict[category],
                title=title,
                ctime=ctime,
                href=href,
                code=code
            )
            # yield scrapy.Request(method="GET", url=href, dont_filter=True, callback=self.parse_item,
            #                      meta={'item': item})
            yield item

    def parse_item(self, response):
        item = response.meta["item"]

        print(response.url)
        article = response.xpath('//div[@class="body_main"]//p')
        # 去除句子中的\xa0\xa0，返回列表
        content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
        attachments = article.xpath(
            './/a[contains(@href,".pdf") \
            or contains(@href,".rar") \
            or contains(@href,".doc") \
            or contains(@href,".xls") \
            or contains(@href,".zip") \
            or contains(@href,".docx")]')
        attachments_dict = self.get_attachment(attachments, response.request.url)
        item.update(
            content=content,
            attachments=attachments_dict
        )
        # print(item)
        yield item
