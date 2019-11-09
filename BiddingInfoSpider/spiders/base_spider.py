import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings
from scrapy.selector import Selector
from urllib import parse
from w3lib.html import remove_tags
import re
import time


class BaseSpider(CrawlSpider):
    name = "base_spider"
    website_name = ""
    tmpl_url = ""
    

    def __init__(self, *a, **kw):
        super(BaseSpider, self).__init__(*a, **kw)
        self.follow_links = set()
        settings = get_project_settings()
        self.biddingInfo_update = settings.getbool('BIDDING_INFO_UPDATE', True)

    def unique_follow_links(self, links):
        # 对不同页面获取的列表链接进行去重
        unique_links = []
        for lnk in links:
            if lnk.url not in self.follow_links:
                unique_links.append(lnk)
                self.follow_links.add(lnk.url)
        return unique_links

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # super中会对_follow_links进行一次修改
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        if spider.biddingInfo_update:
            # 只会解析入口页的信息
            spider._follow_links = False
        return spider

    def get_re(self, p, s):
        r = re.findall(p, s, flags=0)
        if r:
            return r
        else:
            print("无法找到数字")

    def get_attachment(self, attachment, ulr):
        '''
        :param attachment: 类型为Select()的a 标签列表
        :param ulr: response.request.url
        :return: dict
        '''
        attachments_dict = dict()
        att_num = 0
        if attachment:
            for a in attachment:
                att_num += 1
                attachment_name = a.xpath('string(.)').extract_first() or ('attachment_no_title_' + str(att_num))
                attachment_href = parse.urljoin(ulr, a.xpath('@href').extract_first())
                attachments_dict.update({attachment_name: attachment_href})
        return attachments_dict

    def get_ctime(self, ctime_select):
        '''select'''
        ctime_str = ''
        if ctime_select.extract():
            ctime_str = (''.join(ctime_select.extract())).strip()
            if '(' in ctime_str:
                ctime_str = ctime_str.replace('(', '').replace(')', '')
            if '[' in ctime_str:
                ctime_str = ctime_str.replace('[', '').replace(']', '')
            if '月' in ctime_str:
                ctime_str = ctime_str = ctime_str.replace('年', '-').replace('月', '-')
            elif '.' in ctime_str:
                ctime_str = ctime_str = ctime_str.replace('.', '-')
            elif '/' in ctime_str:
                ctime_str = ctime_str = ctime_str.replace('/', '-')
            if len(ctime_str) == 5:
                ctime_str = '2018-' + ctime_str

            ctime_list = ctime_str.split('-')
            if len(ctime_list[0]) < 4:
                ctime_str = '20' + ctime_str

            oo = r'\d{4}\-\d{1,2}\-\d{1,2}'
            ctime_str = re.findall(oo, ctime_str)[0]

        return ctime_str


if __name__ == '__main__':
    p = "\'(\d+)\'"
    s = "showProjectDetail(\'014002007\',\'9990000000010326539\');"
    x = re.findall(p, s)
    print(x)
