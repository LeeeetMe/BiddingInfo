from BiddingInfoSpider.spiders.GG import GG


class shanxi0(GG):
    name = 'shanxi0'
    endPageNum = 2

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.area = "陕西"
        if not self.biddingInfo_update:
            self.endPageNum = 50
            self.currTime = self.time_interval.get("近十天")


