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
    print("得到的页数为：", ttlpage)
