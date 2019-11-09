import json
import scrapy
from scrapy import Selector
from scrapy import FormRequest
from urllib.parse import urljoin
from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class BJGongCheng_KanCha(BaseSpider):
    name = 'BJGongCheng_KanCha'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx'
    pageIndex = 1
    category = "建设工程"
    industry = "勘察设计"

    def __init__(self, *a, **kw):
        super(BJGongCheng_KanCha, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 2

    def start_requests(self):
        for i in range(1, self.pageIndex):
            form_data = {
                "PagerControl1": "_ctl4: {0}".format(i)
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True)
            yield request

    def parse_page(self, response):
        res = Selector(response)
        li_lst = res.xpath('//tr[@class="gridview1_RowStyle"]')
        for l in li_lst:
            item = BiddinginfospiderItem()
            a = l.xpath(".//a")
            title = a.xpath('.//text()').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            c = l.xpath('.//td[@class="gridview_RowTD"][last()]')
            ctime = self.get_ctime(c)
            item.update(
                category=self.category,
                industry=self.industry,
                title=title,
                ctime=ctime,
                href=href,
            )
            yield scrapy.Request(url=href, dont_filter=True, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        item = response.meta['item']
        # 主体
        res = Selector(response)
        code = res.xpath('//span[@id="project_no"]//text()').extract_first()
        main = res.xpath('//td')
        # 正文
        content = ["".join(i.split()) for i in main.xpath('normalize-space(string(.))').extract()]
        # 附件
        attach = main.xpath(
            './/a[contains(@href,".pdf") or contains(@href,".rar") or contains(@href,".doc") or contains(@href,".xls") or contains(@href,".zip") or contains(@href,".docx")]')
        attachments = self.get_attachment(attach, response.request.url)
        item['attachments'] = attachments
        item.update(attachments=attachments, content=content, code=code)
        yield item


class BJGongCheng_ShiGong(BJGongCheng_KanCha):
    name = 'BJGongCheng_ShiGong'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_sgzbgg.aspx'
    pageIndex = 1
    category = "建设工程"
    industry = "施工"

    def __init__(self, *a, **kw):
        super(BJGongCheng_ShiGong, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 3


class BJGongCheng_JianLi(BJGongCheng_KanCha):
    name = 'BJGongCheng_JianLi'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_jlzbgg.aspx'
    pageIndex = 1
    category = "建设工程"
    industry = "监理"

    def __init__(self, *a, **kw):
        super(BJGongCheng_JianLi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 3


class BJGongCheng_ZhuanYe(BJGongCheng_KanCha):
    name = 'BJGongCheng_ZhuanYe'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_zyzbgg.aspx'
    pageIndex = 1
    category = "建设工程"
    industry = "专业"

    def __init__(self, *a, **kw):
        super(BJGongCheng_ZhuanYe, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 4


class BJGongCheng_CaiLiao(BJGongCheng_KanCha):
    name = 'BJGongCheng_CaiLiao'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_clsbzbgg.aspx'
    pageIndex = 1
    category = "建设工程"
    industry = "材料设备"

    def __init__(self, *a, **kw):
        super(BJGongCheng_CaiLiao, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 3


class BJGongCheng_TieLu(BJGongCheng_KanCha):
    name = 'BJGongCheng_TieLu'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_tdzbgg.aspx'
    pageIndex = 1
    category = "建设工程"
    industry = "铁路"

    def __init__(self, *a, **kw):
        super(BJGongCheng_TieLu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 6


class BJGongCheng_YuanLin(BJGongCheng_KanCha):
    name = 'BJGongCheng_YuanLin'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_ylzbgg.aspx'
    pageIndex = 1
    category = "建设工程"
    industry = "园林"

    def __init__(self, *a, **kw):
        super(BJGongCheng_YuanLin, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 4


class BJGongCheng_MinHang(BJGongCheng_KanCha):
    name = 'BJGongCheng_MinHang'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_mhzbgg.aspx'
    pageIndex = 2
    category = "建设工程"
    industry = "民航"

    def __init__(self, *a, **kw):
        super(BJGongCheng_MinHang, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 2


class BJGongCheng_JunDui(BJGongCheng_KanCha):
    name = 'BJGongCheng_JunDui'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_jdzbgg.aspx'
    pageIndex = 2
    category = "建设工程"
    industry = "军队"

    def __init__(self, *a, **kw):
        super(BJGongCheng_JunDui, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 2


class BJGongCheng_QiTa(BJGongCheng_KanCha):
    name = 'BJGongCheng_QiTa'
    allowed_domains = ['bcactc.com']
    start_urls = ['http://www.bcactc.com/home/gcxx/now_kcsjzbgg.aspx']
    website_name = '北京市工程建设交易信息网'
    tmpl_url = 'http://www.bcactc.com/home/gcxx/now_qtzbgg.aspx'
    pageIndex = 2
    category = "建设工程"
    industry = "其他"

    def __init__(self, *a, **kw):
        super(BJGongCheng_QiTa, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.pageIndex = 2
