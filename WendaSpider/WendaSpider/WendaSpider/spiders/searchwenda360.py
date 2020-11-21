import scrapy
from WendaSpider.property import Wenda360Property

#弃用，用百度搜索
class Searchwenda360Spider(scrapy.Spider):
    name = 'searchwenda360'
    allowed_domains = ['wenwen.sogou.com']
    #pc端
    # def start_requests(self):
    #     for i in range(len(Wenda360Property.lstSearchKey)):
    #         for j in range(91,Wenda360Property.dictRequirePage[Wenda360Property.lstSearchKey[i]]):
    #             url='https://wenda.so.com/search/?src=srp_suggst_wenda'+'&q='+Wenda360Property.lstSearchKey[i]+'&pn='+str(j)
    #             yield scrapy.Request(url=url, callback=self.parse)
    #     pass
    #
    #
    # def parse(self, response):
    #     qNums = response.xpath('//*[@id="js-qa-list"]/li[@class="item js-normal-item"]/div[1]/h3/a/@href')
    #     qTitles = response.xpath('//*[@id="js-qa-list"]/li[@class="item js-normal-item"]/div[1]/h3/a')
    #     with open('./Url360.csv', 'a')as ofile:
    #         for i in range(len(qNums)):
    #             ofile.write('https://wenda.so.com'+qNums[i].root+','+self.strQ2B(qTitles[i].xpath('string(.)')[0].root)+"\n")
    #     pass

    #手机端
    def start_requests(self):
        for i in range(500):
            url = 'https://wenda.so.com/search/?q=%E6%95%99%E8%82%B2&pn='+str(i)
            #url = 'https://wenda.so.com/search/?q=%E7%A8%8E&pn='+str(i)
            yield scrapy.Request(url=url, callback=self.parse)
        pass

    def parse(self, response):

        pass

    # 半角转全角
    def strQ2B(self, ustring):
        rstring = ""
        for uchar in ustring:
            if uchar == ',':
                uchar = '，'
            rstring += uchar
        return rstring

