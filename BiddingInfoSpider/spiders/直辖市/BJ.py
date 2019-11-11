from BiddingInfoSpider.spiders.GG import GG


class BEIJING(GG):
    name = 'BJ'
    endPageNum = 2
    currTime = "当天"

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.area = "北京"
        if not self.biddingInfo_update:
            self.endPageNum = 6
            self.currTime = "近十天"
