from scrapy.commands import ScrapyCommand  
from scrapy.crawler import CrawlerRunner
from scrapy.exceptions import UsageError
from scrapy.utils.conf import arglist_to_dict


#详版
# class Command(ScrapyCommand):
#
#     requires_project = True
#
#     def syntax(self):
#         return '[options]'
#
#     def short_desc(self):
#         return 'Runs all of the spiders'
#
#     def add_options(self, parser):
#         ScrapyCommand.add_options(self, parser)
#         parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
#                           help="set spider argument (may be repeated)")
#         parser.add_option("-o", "--output", metavar="FILE",
#                           help="dump scraped items into FILE (use - for stdout)")
#         parser.add_option("-t", "--output-format", metavar="FORMAT",
#                           help="format to use for dumping items with -o")
#
#     def process_options(self, args, opts):
#         ScrapyCommand.process_options(self, args, opts)
#         try:
#             opts.spargs = arglist_to_dict(opts.spargs)
#         except ValueError:
#             raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
#
#     def run(self, args, opts):
#         #settings = get_project_settings()
#         spider_loader = self.crawler_process.spider_loader
#         for spidername in args or spider_loader.list():
#             print("*********cralall spidername************" + spidername)
#             self.crawler_process.crawl(spidername, **opts.spargs)
#
#         self.crawler_process.start()

#简版
class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spiders.list()
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
            print('这个时候,名为<' + name+'>的爬虫偷摸地启动了......')
        self.crawler_process.start()

