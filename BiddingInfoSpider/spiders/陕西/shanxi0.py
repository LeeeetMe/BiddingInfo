from BiddingInfoSpider.spiders.GG import GG


class shanxi0(GG):
    name = 'shanxi0'
    endPageNum = 2

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.area = "陕西"


