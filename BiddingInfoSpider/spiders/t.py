from xpinyin import Pinyin

x = """


class {0}(GG):
    name = '{1}'
    area = "{2}"
"""
ll = [
    "北京",
    "天津",
    "河北",
    "山西",
    "内蒙古",
    "辽宁",
    "吉林",
    "黑龙江",
    "上海",
    "江苏",
    "浙江",
    "安徽",
    "福建",
    "江西",
    "山东",
    "河南",
    "湖北",
    "湖南",
    "广东",
    "广西",
    "海南",
    "重庆",
    "四川",
    "贵州",
    "云南",
    "西藏",
    "陕西",
    "甘肃",
    "青海",
    "宁夏",
    "新疆",
    "兵团",
]
if __name__ == '__main__':
    # 实例拼音转换对象
    p = Pinyin()
    print()
    for i in ll:
        base_p = p.get_pinyin(i, '')
        name = base_p+"Area"
        class_name = base_p.upper()
        area = i
        print(x.format(class_name, name, area))
