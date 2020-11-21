import scrapy
from WendaSpider.property import SougouwenwenProperty

#弃用，用必应搜索
class SearchsougouwenwenSpider(scrapy.Spider):
    name = 'searchsougouwenwen'
    allowed_domains = ['https://wenwen.sogou.com/']

    def start_requests(self):
        for i in range(len(SougouwenwenProperty.lstSearchKey)):
            for j in range(SougouwenwenProperty.dictRequirePage[SougouwenwenProperty.lstSearchKey[i]]):
                url = SougouwenwenProperty.strUrlSearchPre + '&query=' + SougouwenwenProperty.lstSearchKey[
                    i] + '&page=' + str(j)
                yield scrapy.Request(url=url, callback=self.parse)
        pass

    def parse(self, response):
        qNums = response.xpath('//*[@id="main"]/div[2]/div/div[@class="vrwrap"]/h3/a/@href')
        qTitles = response.xpath('//*[@id="main"]/div[2]/div/div[@class="vrwrap"]/h3/a')
        with open('./UrlSougou.csv', 'a')as ofile:
            for i in range(len(qNums)):
                ofile.write('https://www.sogou.com' + qNums[i].root + ',' + self.strQ2B(
                    qTitles[i].xpath('string(.)')[0].root) + "\n")
        pass

    # 半角转全角
    def strQ2B(self, ustring):
        rstring = ""
        for uchar in ustring:
            if uchar == ',':
                uchar = '，'
            rstring += uchar
        return rstring
