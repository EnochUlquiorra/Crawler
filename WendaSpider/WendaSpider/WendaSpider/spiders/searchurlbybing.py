import scrapy
from WendaSpider.property import SearchBingProperty

#pc端

class SearchurlbybingSpider(scrapy.Spider):
    name = 'searchurlbybing'
    allowed_domains = ['cn.bing.com']
    #start_urls = ['https://cn.bing.com/search?q=税+site%3azhidao.baidu.com&first=31']
    
    def start_requests(self):
        for website in SearchBingProperty.lstWebSite:
            self.current_website=website         
            for searchkeyone in SearchBingProperty.lstSearchKey6:
                for searchkeytwo in SearchBingProperty.lstSearchKey7:
                    searchkey = searchkeyone +searchkeytwo
                    for i in range(len(SearchBingProperty.lstTimeSlot) - 1):
                        self.flag = True
                        for j in range(100):
                            if self.flag:
                                url = SearchBingProperty.strUrlSearchPre.format(SearchBingProperty.lstTimeSlot[i],
                                                                                SearchBingProperty.lstTimeSlot[i + 1], searchkey,
                                                                                website, j * 1)
                                yield scrapy.Request(url=url, callback=self.parse)
        pass

    def parse(self, response):
        if not self.flag:
            pass
        self.judge(response)

        urls = titles = None
        try:
            urls = response.xpath('//*[@id="b_results"]/li[@class="b_algo"]/h2/a/@href')
            titles = response.xpath('//*[@id="b_results"]/li[@class="b_algo"]/h2/a')
        except:
            print('找不到该元素')
        if urls and titles:
            with open('./Url_baidu_67.csv', 'a',encoding="utf-8")as ofile:
                for i in range(len(urls)):
                    strUrl=urls[i].root
                    strTitle=self.strQ2B(titles[i].xpath('string(.)')[0].root)
                    #if strTitle.find('教育')>=0:
                    ofile.write(strUrl + ',' + strTitle + ',' + self.current_website + "\n")

        pass


    def judge(self, response):
        ele = None
        try:
            ele = response.xpath('//a[@title="下一页"]//text()')[0].root
        except:
            print('找不到该元素')
        finally:
            if not ele or ele != '下一页':
                self.flag = False
                
    # 半角转全角
    def strQ2B(self, ustring):
        rstring = ""
        for uchar in ustring:
            if uchar == ',':
                uchar = '，'
            rstring += uchar
        return rstring