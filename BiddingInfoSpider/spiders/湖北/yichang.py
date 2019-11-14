from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest


class YiChangShigong(BaseSpider):
    name = 'YiChang_Shigong'
    allowed_domains = ['ggzyjy.zgzhijiang.gov.cn']
    start_urls = ['http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003001/003001001/003001001001/?pageing=1']
    website_name = '宜昌市公共资源交易中心'
    tmpl_url = "http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003001/003001001/003001001001/?pageing={0}"
    category = "工程建设"
    industry = "施工"

    def __init__(self, *a, **kw):
        super(YiChangShigong, self).__init__(*a, **kw)
        self.website_name = self.website_name + "-" + self.industry
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 24)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = response.xpath('//li[@class="list-item"]')
        for l in li:
            item = BiddinginfospiderItem()
            a = l.xpath('./a')
            title = a.xpath('.//@title').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            ctime = self.get_ctime(a.xpath('.//span//text()'))
            item.update(
                industry=self.industry,
                category=self.category,
                title=title,
                ctime=ctime,
                href=href,
            )
            yield item
            # yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        item = response.meta["item"]

        print(response.url)
        article = response.xpath('//div[@id="mainContent"]//p')
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


class YiChangJianLi(YiChangShigong):
    name = 'YiChang_JianLi'
    start_urls = ['http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003001/003001001/003001001002/?pageing=1']
    website_name = '宜昌市公共资源交易中心'
    tmpl_url = "http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003001/003001001/003001001002/?pageing={0}"
    category = "工程建设"
    industry = "监理"

    def __init__(self, *a, **kw):
        super(YiChangJianLi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 3)])


class YiChang_KanChaSheJi(YiChangShigong):
    name = 'YiChang_KanChaSheJi'
    start_urls = ['http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003001/003001001/003001001003/?pageing=1']
    website_name = '宜昌市公共资源交易中心'
    tmpl_url = "http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003001/003001001/003001001003/?pageing={0}"
    category = "工程建设"
    industry = "勘察设计"

    def __init__(self, *a, **kw):
        super(YiChang_KanChaSheJi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 4)])


class YiChang_QiTa(YiChangShigong):
    name = 'YiChang_QiTa'
    start_urls = ['http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003001/003001001/003001001004/?pageing=1']
    website_name = '宜昌市公共资源交易中心'
    tmpl_url = 'http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003001/003001001/003001001004/?pageing={0}'
    category = "工程建设"
    industry = "其他"

    def __init__(self, *a, **kw):
        super(YiChang_QiTa, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 4)])


class YiChang_HuoWu(YiChangShigong):
    name = 'YiChang_HuoWu'
    start_urls = ['http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003002/003002001/003002001001/?pageing=1']
    website_name = '宜昌市公共资源交易中心'
    tmpl_url = 'http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003002/003002001/003002001001/?pageing={0}'
    category = "政府采购"
    industry = "货物"

    def __init__(self, *a, **kw):
        super(YiChang_HuoWu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 23)])


class YiChang_FuWu(YiChangShigong):
    name = 'YiChang_FuWu'
    start_urls = ['http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003002/003002001/003002001002/?pageing=1']
    website_name = '宜昌市公共资源交易中心'
    tmpl_url = 'http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003002/003002001/003002001002/?pageing={0}'
    category = "政府采购"
    industry = "服务"

    def __init__(self, *a, **kw):
        super(YiChang_FuWu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 19)])


class YiChang_GongCheng(YiChangShigong):
    name = 'YiChang_GongCheng'
    start_urls = ['http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003002/003002001/003002001003/?pageing=1']
    website_name = '宜昌市公共资源交易中心'
    tmpl_url = 'http://ggzyjy.zgzhijiang.gov.cn/zjSite/jyxx/003002/003002001/003002001003/?pageing={0}'
    category = "政府采购"
    industry = "工程"

    def __init__(self, *a, **kw):
        super(YiChang_GongCheng, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(i) for i in range(1, 19)])
