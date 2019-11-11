from BiddingInfoSpider.spiders.GG import GG


class BT(GG):
    name = 'bingtuan0'
    endPageNum = 2

    def __init__(self, *a, **kw):
        super(BT, self).__init__(*a, **kw)
        self.area = "兵团"
        if not self.biddingInfo_update:
            self.endPageNum = 6
            self.currTime = self.time_interval.get("近十天")


