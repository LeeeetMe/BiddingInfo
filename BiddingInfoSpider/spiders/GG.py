from datetime import date

from BiddingInfoSpider.spiders.base_spider import BaseSpider
from BiddingInfoSpider.items import BiddinginfospiderItem
import scrapy
from urllib.parse import urljoin
from scrapy import FormRequest
import json


class GG(BaseSpider):
    name = 'BG'
    allowed_domains = ['ss.ebnew.com/']
    start_urls = []
    website_name = '全国公共资源交易平台'
    tmpl_url = 'http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp'
    endPageNum = 1

    sheng = {"不限": "0",
             "北京": "110000",
             "天津": "120000",
             "河北": "130000",
             "山西": "140000",
             "内蒙古": "150000",
             "辽宁": "210000",
             "吉林": "220000",
             "黑龙江": "230000",
             "上海": "310000",
             "江苏": "320000",
             "浙江": "330000",
             "安徽": "340000",
             "福建": "350000",
             "江西": "360000",
             "山东": "370000",
             "河南": "410000",
             "湖北": "420000",
             "湖南": "430000",
             "广东": "440000",
             "广西": "450000",
             "海南": "460000",
             "重庆": "500000",
             "四川": "510000",
             "贵州": "520000",
             "云南": "530000",
             "西藏": "540000",
             "陕西": "610000",
             "甘肃": "620000",
             "青海": "630000",
             "宁夏": "640000",
             "新疆": "650000",
             "兵团": "660000", }
    time_interval = {
        "当天": "01",
        "近三天": "02",
        "近十天": "03",
        "近一月": "04",
        "近三月": "05",
        "自定义日期": "06",
    }
    beginTime = "2019-10-31"
    endTime = (date.today()).strftime("%Y-%m-%d")

    def __init__(self, *a, **kw):
        super(GG, self).__init__(*a, **kw)
        self.area = "北京"
        if not self.biddingInfo_update:
            self.endPageNum = 2
            self.currTime = self.time_interval.get("近十天 ")

    def start_requests(self):
        for i in range(1, self.endPageNum):
            form_data = {
                "TIMEBEGIN_SHOW": "2019-10-31",
                "TIMEEND_SHOW": "2019-11-09",
                "TIMEBEGIN": "2019-10-31",
                "TIMEEND": "2019-11-09",
                # 1省平台 2央企招投标
                "SOURCE_TYPE": "1",
                # 01当天，02近三天 03近十天 04一个月 05三个月 06 自定义日期，与上边日期关联
                "DEAL_TIME": self.currTime,
                "DEAL_CLASSIFY": "00",
                # 0000不限、0001交易公告、0002成交公式
                "DEAL_STAGE": "0000",
                # 省、直辖市
                "DEAL_PROVINCE": self.sheng.get(self.area),
                # 下级城市/区
                "DEAL_CITY": "0",

                "DEAL_PLATFORM": "0",
                "BID_PLATFORM": "0",
                "DEAL_TRADE": "0",
                "isShowAll": "1",
                # 第几页
                "PAGENUMBER": str(i),
                # 搜索关键字
                "FINDTXT": "",
            }
            request = FormRequest(self.tmpl_url, callback=self.parse_page, formdata=form_data, dont_filter=True)
            yield request

    def parse_page(self, response):
        print('request_url= ', response.request.url)
        body = json.loads(str(response.body, "utf-8"))
        li = body.get("data")
        print("Num :", len(li))
        for l in li:
            item = BiddinginfospiderItem()
            sheng = l.get('districtShow')
            shiQu = l.get('platformName')
            shi = self.getSHI(shiQu)

            href = l.get("url"),
            if isinstance(href, tuple):
                href = href[0]
            print("href is,", href)
            # href = href.replace("a", "b")
            item.update(
                city=sheng + "-" + shi if shi else sheng,
                title=l.get("title"),
                ctime=l.get("timeShow"),
                category=l.get("classifyShow"),
                href=href,
                industry=l.get("tradeShow"),
            )
            print("ITEM IS")
            print(item)
            # yield item

    def getSHI(self, shiQu):
        shi = ""
        if shiQu:
            if "区" in shiQu and "市" not in shiQu:
                shi = shiQu.split("区")[0]
            elif "市" in shiQu and "区" not in shiQu:
                shi = shiQu.split("市")[0]
            elif "区" in shiQu and "市" in shiQu:
                tmpShiQu = shiQu.split("区")[0]
                if "市" in tmpShiQu:
                    shi = tmpShiQu.split("市")[1]
        return shi
