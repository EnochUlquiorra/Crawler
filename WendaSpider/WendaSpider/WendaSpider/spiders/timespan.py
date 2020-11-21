import scrapy
from WendaSpider.property import SearchBingProperty

#根据每个月的搜索结果数，划分搜索的时间段，因为搜索引擎只能搜索到1000条数据

#pc端
class TimespanSpider(scrapy.Spider):
    name = 'timespan'
    allowed_domains = ['cn.bing.com']
    start_urls = ['http://cn.bing.com/']


    def start_requests(self):
        for website in SearchBingProperty.lstWebSite:
            for searchkey in SearchBingProperty.lstSearchKey:
                for i in range(len(SearchBingProperty.lstTimeSlot) - 1):
                    url = SearchBingProperty.strUrlSearchPre.format(SearchBingProperty.lstTimeSlot[i],
                                                                     SearchBingProperty.lstTimeSlot[i + 1], searchkey,
                                                                     website, 1)
                    yield scrapy.Request(url=url, callback=self.parse)

        pass

    def parse(self, response):
        str_result_num=response.xpath('string(//div[@id="b_tween"]/span[@class="sb_count"])')[0].root
        result_num=int(str_result_num.split(' ')[-2].replace(',',''))
        step=int(30/(int(result_num/1000)+1))
        with open('time_step.txt','a')as ofile:
            ofile.write(str(step)+',')
        pass
