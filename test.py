def get_swf(s):
    start = s.index("escape('")
    end = s.index("'), EncodeURI ")
    result = s[start + 8:end]
    return result


import requests, json

if __name__ == '__main__':
    s = '''var fp = new FlexPaperViewer( 'http://bulletin.jszbtb.com/FlexPaperViewer', 'viewerPlaceHolder', { config : { SwfFile : escape('http://bulletin.jszbtb.com/project//2019-09/noticeFile/Z1101000188J00437001/afd13bf07a824d61bf9f1c412b45f43a.swf'), EncodeURI : true, Scale : 0.6, ZoomTransition : 'easeOut', ZoomTime : 0.5, ZoomInterval : 0.2, FitPageOnLoad : true, FitWidthOnLoad : true, PrintEnabled: false,//是否支持打印 FullScreenAsMaxWindow : false, ProgressiveLoading : true, MinZoomSize : 0.2, MaxZoomSize : 5, SearchMatchAll : false, InitViewMode : 'Portrait', ViewModeToolsVisible : true, ZoomToolsVisible : true, NavToolsVisible : true, CursorToolsVisible : true, SearchToolsVisible : true, localeChain : 'zh_CN' } }); '''
    x = s.index("escape('")
    y = s.index("'), EncodeURI ")
    print(x, y)
    print()

    s = "downloadAnnex('http://www.lyszb.com:82/ProjIndex/doDownload?fid=20369132E0082B9C3E6CCFAC546617EC','0')"
    a = s[15:-6]
    print(a)

{"TABLENAME": "zfcg_notice", "REGIONCODE": "140601", "URL": "/zfcg/zfcgZCNotice/form?id=",
 "HTTPURL": "/noticeDetail?tableName=zfcg_notice=", "PROJECTCODE": "ZZBYFW2019-1017001",
 "ID": "b79de235dd43456cba4da75125abc5ed", "PROJECTNAME": "网络线路租赁项目竞争性磋商公告", "RECEIVETIME": "2019-11-06",
 "FABUPX_TIME": 1573002000000, "ROWNUM_": 1},

category_dict = {
    'gcjs_notice': "工程建设",
    'zfcg_notice': "政府采购",
    'td_notice': "土地使用权",
    'ky_notice': "矿业权出让",
    'gycqsw_notice': "国有产权（实物）",
    'gycqgq_notice': "国有产权（股权）",
}

"moreInfoController.do?getNoticeDetail&url=/gcjs/gcjsNotice/form?id=&id=60abaae604f64b5a803ab57557d1d74f"
"moreInfoController.do?getNoticeDetail&url=/gcjs/gcjsNotice/form?id=&id=60abaae604f64b5a803ab57557d1d74f"

"http://szggzy.shuozhou.gov.cn/moreInfoController.do?getNoticeDetail&url=/zfcg/zfcgZCNotice/form?id=&id=b79de235dd43456cba4da75125abc5ed"
"http://szggzy.shuozhou.gov.cn/moreInfoController.do?getNoticeDetail&url=/zfcg/zfcgZCNotice/form?id=&id=b79de235dd43456cba4da75125abc5ed"
"http://szggzy.shuozhou.gov.cn/moreInfoController.do?getNoticeDetail&url=/zfcg/zfcgZCNotice/form?id=id=&b79de235dd43456cba4da75125abc5ed"

""""
ownerdeptname":"晋江市高铁新城开发建设有限责任公司",
"costDept":"",
"tag":0,
"projNo":"晋政施招20191030075",
"totalInvest":918.801,
"fundSource":"企业自筹",
"planBgDate":"",
"projTradeType":"1",
"applybid":0,
"planEdDate":"",
"buildArea":"晋江市梧垵安置地块",
"projName":"晋江市梧垵安置地块220千伏、110千伏线路迁改项目",
"serviceCharge":80,
"agentDept":"厦门天亚工程项目管理有限公司"""

"""
http://120.27.213.103/ebid/com.hymake.fjbid.comm.viewTask.filesDownload.flow?FileName=-4267_1194076BCC1046D3BDA38211810081EE.pdf&FilePath=%5CUPLOADS%5C7353%5CZBWJ%5C&oldFileName=%E5%85%AC%E5%91%8A%E6%96%87%E4%BB%B6.pdf
fujian/ftp/saveData/I3505000129992085001/TENDER_NOTICE_EXT/6F1B759A-BF37-C67E-9188-FC9E35E7CFFF.zip
"""

if __name__ == '__main__':
    form_data = {
        "TIMEBEGIN_SHOW": "",
        "TIMEEND_SHOW": "",
        "TIMEBEGIN": "",
        "TIMEEND": "",
        "SOURCE_TYPE": "1",
        "DEAL_TIME": "02",
        "DEAL_CLASSIFY": "00",
        "DEAL_STAGE": "0000",
        "DEAL_PROVINCE": "220000",
        "DEAL_CITY": "0",
        "DEAL_PLATFORM": "0",
        "BID_PLATFORM": "0",
        "DEAL_TRADE": "0",
        "isShowAll": "1",
        "PAGENUMBER": "1",
        "FINDTXT": "",
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = json.loads(
        requests.post(
            headers=headers,
            url="http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp",
            data=form_data).text)
    ttlpage = data.get("ttlpage", 1)
    # print("得到的页数为：", ttlpage)

"""
中国化工装备招投标交易平台
中国兵器电子招标投标交易平台
中国电力设备信息网电子招标交易平台
中国长江三峡集团公司电子采购平台
中国石化电子招标投标交易平台
中国交建物资采购管理信息系统
中国交建装备采购管理信息系统
国家电网公司电子商务平台
中国兵器装备集团有限公司招标投标交易平台
国电集团电子招投标平台
中国石化电子招标投标交易平台
国家开发投资公司电子采购平台
南水北调中线建管局招标采购交易平台
航空工业电子采购平台电子招投标专区
中国移动电子采购与招标投标系统
神华招标网
中国石油电子招投标交易平台
中国铁物电子招投标平台
中航招标平台
中煤电子招投标平台
大唐电子商务平台
中国大唐集团公司电子商务平台
中铁建电子采购平台
中国航天科技电子采购平台
招商局集团电子招标采购交易平台
中国华电集团公司电子商务平台
航发网上商城电子招投标专区
中国华能集团电子招投标系统
冀中能源集团招标投标电子交易平台
内蒙古电力集团电子商务系统
鞍钢集团电子招标投标交易平台
中国一汽电子招标采购交易平台
吉林国投招标投标交易平台
上海宝华电子招投标交易平台
中交舟山公司招标采购平台
浪潮集团采购电子商务平台
东风招投标交易中心电子交易平台
武钢电子招标投标平台
中国南方电网电子商务系统

	        			</select>
"""

"http://epp.ctg.com.cn/infoview/?fileId=18bcb843b41140a595d5553db91eb2f1&openFor=ZBGG&typeFor=undefined"
"18bcb843b41140a595d5553db91eb2f1"

if __name__ == '__main__':
    xx = "http://ec.ccccltd.cn/PMS/gysCggg.shtml?id=rlfE3i5BGBB0+4B90Mn5NFqXO9o+RLfH6jsITwDEk951zLidmyWYgOWEs0LitWGffQOR1c8LTcIdDnNNdYmzxoE1tptSk0DTfQOR1c8LTcIdDnNNdYmzxsiljOcgldaaGlc9rVi95hCedxzq7qFZuZ9zkhWTvizjGPvNdUTZd5ZWRFxeAJJDCVtXDy8n/F1o"
    x = '''"javaScript:goByDetail('rlfE3i5BGBB0+4B90Mn5NFqXO9o+RLfH6jsITwDEk951zLidmyWYgOWEs0LitWGffQOR1c8LTcId\r\nDnNNdYmzxoE1tptSk0DTfQOR1c8LTcIdDnNNdYmzxsiljOcgldaaGlc9rVi95hCedxzq7qFZuZ9z\r\nkhWTvizjGPvNdUTZd5ZWRFxeAJJDCVtXDy8n/F1o');"'''
    y = x[24:-4]
    # print(y)

"rlfE3i5BGBB0+4B90Mn5NFqXO9o+RLfH6jsITwDEk951zLidmyWYgOWEs0LitWGffQOR1c8LTcIdDnNNdYmzxjUB1hNMt9PyfQOR1c8LTcIdDnNNdYmzxvG/ysgm7VmLx+GoNFRm87WA+IuHqMW44uWBS/i8tTd8GPvNdUTZd5ZWRFxeAJJDCVtXDy8n/F1o"
"rlfE3i5BGBB0+4B90Mn5NFqXO9o+RLfH6jsITwDEk951zLidmyWYgOWEs0LitWGffQOR1c8LTcIdDnNNdYmzxjUB1hNMt9PyfQOR1c8LTcIdDnNNdYmzxvG/ysgm7VmLx+GoNFRm87WA+IuHqMW44uWBS/i8tTd8GPvNdUTZd5ZWRFxeAJJDCVtXDy8n/F1o"
"sjN7r9ttBwLI2dpg4DQpQb68XreXjaqkgAGKY+PrnM/uM6hTdytqaAowtvisBTZxgZQI4K+0VHY/rDSoXkZRejld1QARSP2y3zSEjSIQ0DlH3dRNK+L0Yq5Xyb5gMh+OGVwHeA8nQj8yaKl8Yr0+nw=="

if __name__ == '__main__':
    response = requests.get("http://localhost:8000/get")
    print(response.status_code)
    x = json.loads(response.text)
    print()
