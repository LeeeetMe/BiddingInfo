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
    'TianJin', "TaiYuan_ShiGong", 'henanArea', 'hubeiArea', 'hunanArea', 'guangdongArea', 'guangxiArea', 'hainanArea',
    'chongqingArea', 'sichuanArea', 'guizhouArea', 'yunnanArea', 'xizangArea', 'shanxiArea', 'gansuArea', 'qinghaiArea',
    'ningxiaArea', 'xinjiangArea', 'bingtuanArea',
    'wugang', 'dongfeng', 'langchao', 'yiqi', 'angang', 'nmgdl', 'jzny', 'hangfa', 'huadian', 'zhaoshangju',
    'tiejiansb', 'tiejianwz', 'datang', 'zhongmei', 'zhonghang', 'zhongtiewu',
    'HuaGongZhaoBiao', 'BingQiDianZi', 'DianLiSheBei', 'ChangJiangSanXia', 'ZhongShiHua',
    'JiaoJianWuZi', 'KaiFaTouZi', 'NanShuiBeiDiao', 'HangKongGongYe', 'YiDongDianZi',
    'ShenHua', 'ShenHuaFuWu', 'ShenHuaGongCheng',
    'beijingArea', 'tianjinArea', 'hebeiArea', 'shanxiXArea', 'neimengguArea', 'liaoningArea', 'jilinArea',
    'heilongjiangArea', 'shanghaiArea', 'jiangsuArea', 'zhejiangArea', 'anhuiArea', 'fujianArea', 'jiangxiArea',
    'shandongArea',

]

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute([
    "scrapy",
    "crawl",
    # spider_list[-1]
    'YiDongDianZi',
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
