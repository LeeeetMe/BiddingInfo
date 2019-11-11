from BiddingInfoSpider.spiders.GG import GG


class xizang0(GG):
    name = 'xizang0'
    endPageNum = 2

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.area = "西藏"
        if not self.biddingInfo_update:
            self.endPageNum = 20
            self.currTime = self.time_interval.get("近十天")


