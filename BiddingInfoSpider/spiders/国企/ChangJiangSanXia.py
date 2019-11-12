import json

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem


class ChangJiangSanXia(BaseSpider):
    name = 'ChangJiangSanXia'
    allowed_domains = ['epp.ctg.com.cn']
    start_urls = ['http://epp.ctg.com.cn/index/getData.do?queryName=ctg.list.zbgg&page=1&rows=15']
    website_name = '中国长江三峡集团公司电子采购平台'
    tmpl_url = 'http://epp.ctg.com.cn/index/getData.do?queryName=ctg.list.zbgg&page=1&rows={0}'
    category = ""
    industry = ""

    def __init__(self, *a, **kw):
        super(ChangJiangSanXia, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.start_urls = [self.tmpl_url.format(60)]

    def parse_start_url(self, response):
        print('request_url= ', response.request.url)
        li = json.loads(str(response.body, "utf-8"))
        data = li.get("rows")
        article_tmp_url = "http://epp.ctg.com.cn/infoview/?fileId={0}&openFor=ZBGG&typeFor=undefined"
        for li in data:
            item = BiddinginfospiderItem()
            title = li.get('TITLE')
            ctime = li.get('CREATED_TIME')
            id = li.get('ARTICLE_ID')
            href = article_tmp_url.format(id)
            item.update(
                industry=self.industry,
                category=self.category,
                title=title,
                ctime=ctime,
                href=href,
            )
            # print(item)
            yield item
