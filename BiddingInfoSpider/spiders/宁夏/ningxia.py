from BiddingInfoSpider.spiders.GG import GG


class ningxia(GG):
    name = 'ningxia0'
    endPageNum = 2

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.area = "宁夏"
        if not self.biddingInfo_update:
            self.endPageNum = 6
            self.currTime = self.time_interval.get("近十天")


