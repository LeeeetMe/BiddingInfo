from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy


class EcpSgcc(BaseSpider):
    name = 'ecp_sgcc'
    allowed_domains = ['ecp.sgcc.com.cn']
    start_urls = [
        'http://ecp.sgcc.com.cn/topic_project_list.jsp?columnName=topic10&site=global&company_id=00&status=00&project_name=all&pageNo=1']
    website_name = '国家电网有限公司'
    tmpl_url = 'http://ecp.sgcc.com.cn/topic_project_list.jsp?columnName=topic10&site=global&company_id=00&status={0}&project_name=all&pageNo={1}'
    article_tmp = "http://ecp.sgcc.com.cn/html/project/{0}/{1}.html"
    """
    00 默认所有
    2  正在招标
    3  已经截标
    4  正在开标
    5  正在评标
    6  招标结束
    7  评标结束
    """
    status = 2

    def __init__(self, *a, **kw):
        super(EcpSgcc, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = ([self.tmpl_url.format(self.status, i) for i in range(1, 7)])

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        ul = response.xpath("//tr[@align='left']")
        for i in range(1, len(ul)):
            item = BiddinginfospiderItem()
            el = ul[i].xpath(".//td")
            li_a = el[2].xpath('.//a')

            code = el[1].xpath('normalize-space(string(.))').extract_first()
            title = li_a.xpath('@title').extract_first()
            ctime = el[3].xpath('normalize-space(string(.))').extract_first()
            param = li_a.xpath('@onclick').extract_first()
            param_lst = self.get_re("\'(\d+)\'", param)
            href = self.article_tmp.format(param_lst[0], param_lst[1])
            item.update(
                code=code,
                title=title,
                ctime=ctime,
                href=href,
            )
            # req = scrapy.Request(response.urljoin(href), callback=self.parse_item, dont_filter=True,
            #                      meta={'item': item})
            yield item

    def parse_item(self, response):
        item = response.meta.get("item")
        print(response.url)
        article = response.xpath('//table[@class="font02"]')
        content = article.xpath('normalize-space(string(.))').extract_first()
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
