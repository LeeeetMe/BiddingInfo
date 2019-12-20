from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest


class JiaoJianWuZi(BaseSpider):
    name = 'JiaoJianWuZi'
    allowed_domains = ['ec.ccccltd.cn']
    start_urls = []
    website_name = '中国交建物资采购管理信息系统'
    tmpl_url = "http://ec.ccccltd.cn/PMS/gysmore.shtml?id=sjN7r9ttBwLI2dpg4DQpQb68XreXjaqknBMygP8dAEQ57TILyRtTnCZX1hIiXHcc1Ra16D6TzZdblRFD/JXcCd5FP7Ek60ksxl9KkyODirY="
    endPageNum = 2

    def __init__(self, *a, **kw):
        super(JiaoJianWuZi, self).__init__(*a, **kw)
        if not self.biddingInfo_update:
            self.endPageNum = 5

    def start_requests(self):
        for i in range(1, self.endPageNum):
            form_data = {
                "VENUS_PAGE_NO_KEY_INPUT": str(i),
                "VENUS_PAGE_NO_KEY": str(i),
                # "VENUS_PAGE_COUNT_KEY": "2633",
                "VENUS_PAGE_SIZE_KEY": "15",
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data)
            yield request

    def parse_page(self, response):
        res = scrapy.Selector(response)
        article_tmp_url = 'http://ec.ccccltd.cn/PMS/gysCggg.shtml?id={0}'
        li = res.xpath('//td[@class="listCss"]//a')
        for a in li:
            item = BiddinginfospiderItem()
            title = a.xpath('normalize-space(string(.))').get()
            x = "".join(a.xpath('.//@href').get().replace("\\r", "").replace("\\n", "").split())[23:-3]
            href = article_tmp_url.format(x)
            ctime = self.get_ctime(a.xpath('../following-sibling::td[1]//text()'))
            item.update(
                title=title,
                href=href,
                ctime=ctime,
            )
            # print(item)
            yield item
