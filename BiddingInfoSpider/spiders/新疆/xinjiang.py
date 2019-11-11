from BiddingInfoSpider.spiders.GG import GG


class XinJiang(GG):
    name = 'xinjiang0'
    endPageNum = 2

    def __init__(self, *a, **kw):
        super(XinJiang, self).__init__(*a, **kw)
        self.area = "新疆"
        if not self.biddingInfo_update:
            self.endPageNum = 6
            self.currTime = self.time_interval.get("近十天")


