from scrapy.exporters import BaseItemExporter
from BiddingInfoSpider.settings import FIELDS
import xlwt


class ExcelItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file
        self.wbook = xlwt.Workbook()
        self.wsheet = self.wbook.add_sheet('scrapy')  # scrapy 为表格的标签名
        self.row = 0
        # 写入第一行字段
        for col, v in enumerate(FIELDS):
            self.wsheet.write(0, col, v)

    def finish_exporting(self):
        self.wbook.save(self.file)

    def export_item(self, item):
        fields = self._get_serialized_fields(item, include_empty=True)
        for col, v in enumerate(x for _, x in fields):
            self.wsheet.write(self.row + 1, col, v)
        self.row += 1
