from scrapy.cmdline import execute
import sys, os

spider_list = [
    'lhjs', 'ecp_sgcc', 'YiChang_Shigong', 'YiChang_JianLi', 'YiChang_KanChaSheJi',
    'YiChang_QiTa', 'YiChang_HuoWu', 'YiChang_FuWu', 'YiChang_GongCheng', 'BL',
    'GuangDongJianShe', 'GuangDongJiaoTong', 'GuangDongDianLi', 'GuangDongTieLu', 'GuangDongShuiLi',
    'GuangDongYuanLin', 'GuangDongMinHang', 'GuangDongJunDui', 'GuangDongFeiBiXu', 'GuangDongQiTa',
    'ShuoZhou', 'ZhongHaiYou', "ZhongShiYou",
    'JiangSu', 'LongYan_JianShe''suqian', 'shenzhen', 'hainan', 'jinan', 'hebei', 'shandong', 'wuhan', 'guangzhou',
    'putian', 'wuyishan', 'anyang', 'meishan', 'nanping', 'nanwang', 'shaowu', 'jingcaizh', 'henan', 'anhui',
    'HuNan', 'HuBei', 'QuanZhou','qinghai','qinghai2','ganshu'
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
