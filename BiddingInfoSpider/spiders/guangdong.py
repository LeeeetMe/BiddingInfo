from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from scrapy import FormRequest


class GuangDongJianShe(BaseSpider):
    name = 'GuangDongJianShe'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=503&pchannelid=466&curgclb=01,02,14&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=1&cIndex=1']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=503&pchannelid=466&curgclb=01,02,14&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=1&cIndex=1'
    endPageNum = 1
    category = "工程建设"

    def __init__(self, *a, **kw):
        super(GuangDongJianShe, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 16

    def start_requests(self):
        for i in range(1, self.endPageNum):
            form_data = {
                'page': str(i),
                'xmmc': "",
                'xmjdbmid': "",
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True)
            yield request

    def parse_page(self, response):
        print(response.request.url)
        a_lst = response.xpath('//table[@class="wsbs-table"]//a')
        for a in a_lst:
            item = BiddinginfospiderItem()

            title = a.xpath('.//text()').extract_first()
            href = response.urljoin(a.xpath('.//@href').extract_first())
            ctime = self.get_ctime(a.xpath('../../td//text()'))
            item.update(
                title=title,
                ctime=ctime,
                href=href,
            )
            yield scrapy.Request(
                url=href,
                dont_filter=True,
                callback=self.parse_item,
                meta={'item': item})

    def parse_item(self, response):
        item = response.meta.get("item")
        print(response.url)
        article = response.xpath('//div[@class="Section1"]//p')
        # 去除句子中的\xa0\xa0，返回列表
        content = ["".join(i.split()) for i in article.xpath('normalize-space(string(.))').extract()]
        attachments = response.xpath(
            './/a[contains(@href,".pdf") \
            or contains(@href,".rar") \
            or contains(@href,".doc") \
            or contains(@href,".xls") \
            or contains(@href,".zip") \
            or contains(@href,".docx")]')
        attachments_dict = self.get_attachment(attachments, response.request.url)
        item.update(
            content=content,
            attachments=attachments_dict,
        )
        print(item)
        # yield item


class GuangDongJiaoTong(GuangDongJianShe):
    name = 'GuangDongJiaoTong'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=510&channelids=15&pchannelid=467&curgclb=03&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=2']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=510&channelids=15&pchannelid=467&curgclb=03&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=2'
    endPageNum = 2
    category = "交通"

    def __init__(self, *a, **kw):
        super(GuangDongJiaoTong, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 3


class GuangDongDianLi(GuangDongJianShe):
    name = 'GuangDongDianLi'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=515&channelids=15&pchannelid=468&curgclb=05&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=3']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=515&channelids=15&pchannelid=468&curgclb=05&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=3'
    endPageNum = 2
    category = "电力"

    def __init__(self, *a, **kw):
        super(GuangDongDianLi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 2


class GuangDongTieLu(GuangDongJianShe):
    name = 'GuangDongTieLu'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=520&channelids=15&pchannelid=469&curgclb=06&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=4']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=520&channelids=15&pchannelid=469&curgclb=06&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=4'
    endPageNum = 2
    category = "铁路"

    def __init__(self, *a, **kw):
        super(GuangDongTieLu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 2


class GuangDongShuiLi(GuangDongJianShe):
    name = 'GuangDongShuiLi'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=525&channelids=15&pchannelid=470&curgclb=04&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=5']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=525&channelids=15&pchannelid=470&curgclb=04&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=5'
    endPageNum = 2
    category = "水利"

    def __init__(self, *a, **kw):
        super(GuangDongShuiLi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 6


class GuangDongYuanLin(GuangDongJianShe):
    name = 'GuangDongYuanLin'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=543&channelids=15&pchannelid=472&curgclb=08&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=6']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=543&channelids=15&pchannelid=472&curgclb=08&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=6'
    endPageNum = 2
    category = "园林"

    def __init__(self, *a, **kw):
        super(GuangDongYuanLin, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 2


class GuangDongMinHang(GuangDongJianShe):
    name = 'GuangDongMinHang'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=539&channelids=15&pchannelid=471&curgclb=07&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=7']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=539&channelids=15&pchannelid=471&curgclb=07&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=7'
    endPageNum = 2
    category = "民航"

    def __init__(self, *a, **kw):
        super(GuangDongMinHang, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 2


class GuangDongJunDui(GuangDongJianShe):
    name = 'GuangDongJunDui'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=1033&channelids=9999&pchannelid=475&curgclb=&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=8']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=1033&channelids=9999&pchannelid=475&curgclb=&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=8'
    endPageNum = 2
    category = "军队"

    def __init__(self, *a, **kw):
        super(GuangDongJunDui, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 2


class GuangDongFeiBiXu(GuangDongJianShe):
    name = 'GuangDongFeiBiXu'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=530&channelids=15&pchannelid=473&curgclb=&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=9']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=530&channelids=15&pchannelid=473&curgclb=&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=9'
    endPageNum = 2
    category = "非必须招标工程"

    def __init__(self, *a, **kw):
        super(GuangDongFeiBiXu, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 2


class GuangDongQiTa(GuangDongJianShe):
    name = 'GuangDongQiTa'
    allowed_domains = ['www.gzggzy.cn/']
    start_urls = [
        'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=535&channelids=15&pchannelid=474&curgclb=13&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=10']
    website_name = '广东公共交易中心'
    tmpl_url = 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=535&channelids=15&pchannelid=474&curgclb=13&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=10'
    endPageNum = 2
    category = "其他"

    def __init__(self, *a, **kw):
        super(GuangDongQiTa, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 2
