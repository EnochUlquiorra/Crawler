
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


#execute(["scrapy","crawl","searchwenda360"])
#execute(["scrapy","crawl","wenda360"])

#execute(["scrapy","crawl","searchsougouwenwen"])
execute(["scrapy","crawl","sougouwenwen"])

#execute(["scrapy","crawl","searchbaiduzhidao"])

#execute(["scrapy","crawl","searchurlbybing"])

#execute(["scrapy","crawl","searchurlbybaidu"])

#execute(["scrapy","crawl","baiduzhidao"])

#execute(["scrapy","crawl","mybaiduzhidao"])

#execute(["scrapy","crawl","timespan"])

