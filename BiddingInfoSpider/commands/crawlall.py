from scrapy.commands import ScrapyCommand
from scrapy.crawler import CrawlerRunner
from scrapy.exceptions import UsageError
from scrapy.utils.conf import arglist_to_dict


# 详版
# class Command(ScrapyCommand):
#
#     requires_project = True
#
#     def syntax(self):
#         return '[options]'
#
#     def short_desc(self):
#         return 'Runs all of the spiders'
#
#     def add_options(self, parser):
#         ScrapyCommand.add_options(self, parser)
#         parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
#                           help="set spider argument (may be repeated)")
#         parser.add_option("-o", "--output", metavar="FILE",
#                           help="dump scraped items into FILE (use - for stdout)")
#         parser.add_option("-t", "--output-format", metavar="FORMAT",
#                           help="format to use for dumping items with -o")
#
#     def process_options(self, args, opts):
#         ScrapyCommand.process_options(self, args, opts)
#         try:
#             opts.spargs = arglist_to_dict(opts.spargs)
#         except ValueError:
#             raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
#
#     def run(self, args, opts):
#         #settings = get_project_settings()
#         spider_loader = self.crawler_process.spider_loader
#         for spidername in args or spider_loader.list():
#             print("*********cralall spidername************" + spidername)
#             self.crawler_process.crawl(spidername, **opts.spargs)
#
#         self.crawler_process.start()

# 简版
class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()
        # 各个地区
        spider_list = [
            'anhui', 'jinan', 'shandong', 'ShuoZhou', 'TaiYuan_ShiGong',
            'GuangDongJianShe', 'GuangDongJiaoTong', 'GuangDongDianLi', 'GuangDongTieLu', 'GuangDongShuiLi',
            'GuangDongYuanLin', 'GuangDongMinHang', 'GuangDongJunDui', 'GuangDongFeiBiXu', 'GuangDongQiTa',

            # 'guangzhou', 'meishan', 'shenzhen', 'JiangSu', 'suqian',
            # 'hebei', 'anyang', 'henan', 'lhjs', 'hainan',
            # 'HuBei', 'wuhan', 'YiChang_Shigong', 'YiChang_JianLi', 'YiChang_KanChaSheJi',

            # 'YiChang_QiTa', 'YiChang_HuoWu', 'YiChang_FuWu', 'YiChang_GongCheng', 'HuNan',
            # 'ganshu', 'BJGongCheng_KanCha', 'BJGongCheng_ShiGong', 'BJGongCheng_JianLi',
            # 'BJGongCheng_ZhuanYe', 'BJGongCheng_CaiLiao', 'BJGongCheng_TieLu', 'BJGongCheng_YuanLin',
            # 'BJGongCheng_MinHang', 'BJGongCheng_JunDui',
            # #
            # 'BJGongCheng_QiTa',
            # 'TianJin', 'LongYan_JianShe', 'nanping', 'putian', 'shaowu', 'BL',
            # 'wuyishan', 'jingcaizh', 'qinghai', 'BJ',
            # 'shanxi0',
            # ]
            # 全国各省
            # spider_list = [
            # # 东
            # 'beijingArea', 'tianjinArea', 'hebeiArea', 'shanxiXArea', 'neimengguArea',
            # 'liaoningArea', 'jilinArea', 'heilongjiangArea', 'shanghaiArea', 'jiangsuArea',
            # 'zhejiangArea', 'anhuiArea', 'fujianArea', 'jiangxiArea',
            # # 西
            # 'henanArea', 'hubeiArea', 'hunanArea', 'guangdongArea', 'guangxiArea', 'hainanArea',
            # 'chongqingArea', 'sichuanArea', 'guizhouArea', 'yunnanArea', 'xizangArea', 'shanxiArea', 'gansuArea',
            # 'qinghaiArea', 'ningxiaArea', 'xinjiangArea', 'bingtuanArea',
            # ]
            # 国企公司
            # spider_list = [
            # 'BingQiDianZi', 'ChangJiangSanXia', 'DianLiSheBei', 'HangKongGongYe', 'HuaGongZhaoBiao',
            # 'JiaoJianWuZi', 'KaiFaTouZi', 'NanShuiBeiDiao', 'angang', 'datang',
            # 'zhongtiewu', 'zhonghang', 'ZhongHaiYou', 'langchao', 'nanwang',
            # 'dongfeng', 'ecp_sgcc', 'hangfa', 'huadian', 'jzny',
            # 'nmgdl', 'zhongmei', 'tiejiansb', 'tiejianwz', 'zhaoshangju',
            # 'wugang', 'yiqi', 'ZhongShiHua', 'YiDongDianZi',

            # spider_list = [
            # 'ShanDongSWZF', 'ShanDongSWZF', 'ShanDongBT', 'QingDao', 'JiMo',
            # 'QingDaoKX', 'QingDaoKJDT', 'ShanDongKXJST', 'ShanDongKJZX'
            # ]
        ]
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
            print('这个时候,名为<' + name + '>的爬虫偷摸地启动了......')
        self.crawler_process.start()
