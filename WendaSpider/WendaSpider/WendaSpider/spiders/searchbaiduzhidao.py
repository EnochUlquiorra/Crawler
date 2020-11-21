import scrapy
from WendaSpider.property import BaiduzhidaoProperty

#弃用，用必应搜索
class SearchbaiduzhidaoSpider(scrapy.Spider):
    name = 'searchbaiduzhidao'
    #allowed_domains = ['zhidao.baidu.com']
    #start_urls = ['https://cn.bing.com/search?q=税+site%3azhidao.baidu.com&first=31']

    def start_requests(self):
        for i in range(len(BaiduzhidaoProperty.lstSearchKey)):
            for j in range(BaiduzhidaoProperty.dictRequirePage[BaiduzhidaoProperty.lstSearchKey[i]]):
                print(j)
                url='https://cn.bing.com/search?q={}+site%3azhidao.baidu.com&first={}1'.format(BaiduzhidaoProperty.lstSearchKey[i],j)
                #url = BaiduzhidaoProperty.strUrlSearchPre + '&word=' + BaiduzhidaoProperty.lstSearchKey[i] + '&pn=' + str(j*10)
                yield scrapy.Request(url=url, callback=self.parse)
        pass

    def parse(self, response):
        qUrls = response.xpath('//*[@id="b_results"]/li[@class="b_algo"]/div[1]/h2/a[2]/@href')
        qTitles = response.xpath('//*[@id="b_results"]/li[@class="b_algo"]/div[1]/h2/a[2]')

        with open('./Url_baiduzhidao67.csv', 'a')as ofile:
             for i in range(len(qUrls)):
                if self.strQ2B(qTitles[i].xpath('string(.)')[0].root).find('税')>=0:
                    ofile.write(qUrls[i].root + ',' + self.strQ2B(qTitles[i].xpath('string(.)')[0].root) + "\n")
        pass


    # 半角转全角
    def strQ2B(self, ustring):
        rstring = ""
        for uchar in ustring:
            if uchar == ',':
                uchar = '，'
            rstring += uchar
        return rstring