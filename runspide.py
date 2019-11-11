from scrapy.cmdline import execute
import sys, os

spider_list = [
    'lhjs', 'ecp_sgcc', 'YiChang_Shigong', 'YiChang_JianLi', 'YiChang_KanChaSheJi',
    'YiChang_QiTa', 'YiChang_HuoWu', 'YiChang_FuWu', 'YiChang_GongCheng', 'BL',
    'GuangDongJianShe', 'GuangDongJiaoTong', 'GuangDongDianLi', 'GuangDongTieLu', 'GuangDongShuiLi',
    'GuangDongYuanLin', 'GuangDongMinHang', 'GuangDongJunDui', 'GuangDongFeiBiXu', 'GuangDongQiTa',
    'ShuoZhou', 'ZhongHaiYou', "ZhongShiYou",
    'JiangSu', 'LongYan_JianShe''suqian', 'shenzhen', 'hainan', 'jinan', 'hebei', 'shandong', 'wuhan', 'guangzhou',
    'putian', 'wuyishan', 'anyang', 'meishan', 'nanping', 'nanwang', 'shaowu', 'jingcaizh', 'henan',
    'HuNan', 'HuBei', 'QuanZhou', 'qinghai', 'ganshu',
    'BJGongCheng_KanCha', 'BJGongCheng_ShiGong',
    'BJGongCheng_JianLi', 'BJGongCheng_ZhuanYe', 'BJGongCheng_CaiLiao',
    'BJGongCheng_TieLu', 'BJGongCheng_YuanLin', 'BJGongCheng_MinHang', 'BJGongCheng_JunDui', 'BJGongCheng_QiTa',
    'TianJin', "TaiYuan_ShiGong", 'bingtuan0', 'xinjiang0', 'ningxia0', 'qinghai0', 'ganshu0', 'shanxi0', 'xizang0',
    'yunnan0'

]

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute([
    "scrapy",
    "crawl",
    spider_list[-1]
])

# 通过commands目录中的crawlall执行所有爬虫项目
# execute([
#     "scrapy",
#     "crawlall"
# ])

# execute([
#     'scrapy','runspider', '/Users/yunyi/projects/scrapy_projects/policy_wikipedia/policy_wikipedia/spiders/shandong.py'
# ])

# cmdline.execute("scrapy crawl GuangDongJianShe -t csv -o guangdong.csv".split())
