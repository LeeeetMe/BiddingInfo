import json
import scrapy
from scrapy.selector import Selector
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class ShenZhen(BaseSpider):
    name = 'shenzhen'
    allowed_domains = ['zjj.sz.gov.cn']
    start_urls = ['http://zjj.sz.gov.cn/jsjy/jyxx/zbgg/']
    website_name = '深圳市建设工程'
    tmpl_url = ['https://www.szjsjy.com.cn:8001/jyw/queryGongGaoList.do?rows=10&page=%s' % i for i in range(1, 50)]

    def __init__(self, *a, **kw):
        super(ShenZhen, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = self.tmpl_url

    def parse(self, response):
        rs = response.body.decode('utf8')
        rs1 = rs[rs.find('['):-2]
        rs2 = json.loads(rs1)

        for l in rs2:
            title = l['ggName']
            href = l['detailUrl']
            ctime = l['ggStartTime2'][0:9]
            city = '深圳'
            uid = l['ggGuid']
            item = BiddinginfospiderItem(title=title, ctime=ctime, href=href, city=city, )
            # 另一种方法
            # data= {
            #     'ggGuid': uid
            # }
            # yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item,method='POST',body=json.dumps(data),meta={"dynamic": True,} )
            # yield scrapy.Request(
            #     url='https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid=' + uid + '&gcbh=&bdbhs=',
            #     dont_filter=True, callback=self.parse_item, meta={'meta': item, })
            yield item

    def parse_item(self, response):
        item = response.meta['meta']
        # 返回响应为json字符串
        html = json.loads(response.body.decode('utf8'))['html']
        # 利用库中自带的Selector解析字符串html 也可以用lxml库
        selector = Selector(text=html)
        article = selector.xpath('//div[@class="bd_con"]')
        content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
        attach = selector.xpath('//div[@id="upload_file1"]')
        attachments = attach.xpath(
            './/a[contains(text(),".pdf") or contains(text(),".rar") or contains(text(),".doc") or contains(text(),".xls") or contains(@text(),".zip") or contains(@text(),".docx")]')
        attachments_dict = self.get_attachment(attachments, response.request.url)

        item.update(content=content, attachments=attachments_dict, )
        print(item)

