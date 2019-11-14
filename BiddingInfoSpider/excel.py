from scrapy.exporters import BaseItemExporter
from BiddingInfoSpider.settings import FIELDS
import xlwt
from scrapy.extensions.feedexport import FeedExporter

class ExcelItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        print("ExcelItemExporter init")
        self.file = file
        # scrapy 为表格的标签名
        self.row = 0

    def start_exporting(self):
        print("start_exporting")
        self.wbook = xlwt.Workbook()
        self.wsheet = self.wbook.add_sheet('scrapy')
        # 写入第一行字段
        for col, v in enumerate(FIELDS):
            self.wsheet.write(0, col, v)

    def finish_exporting(self):
        print("finish_exporting")
        self.wbook.save(self.file)

    def export_item(self, item):
        print("export_item")
        fields = self._get_serialized_fields(item, include_empty=True)
        for col, v in enumerate(x for _, x in fields):
            self.wsheet.write(self.row + 1, col, v)
        self.row += 1
