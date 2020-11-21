import scrapy
from WendaSpider.property import SearchBaiduProperty


# 移动端
# 通过百度搜索获得问题URL
# 这个URL是通过百度加密的（同个结果不同时间搜索得到的url也不一样，问题去重需要额外想一下）
class SearchurlbybaiduSpider(scrapy.Spider):
    name = 'searchurlbybaidu'
    allowed_domains = ['www.baidu.com']
    flag = True
    current_website=''

    # start_urls = [
    #     'https://www.3dmgame.com/']

    def start_requests(self):
        for website in SearchBaiduProperty.lstWebSite:
            self.current_website=website
            for searchkeyone in SearchBaiduProperty.lstSearchKey20:
                for searchkeytwo in SearchBaiduProperty.lstSearchKey30:
                    searchkey = searchkeyone +searchkeytwo
                    for i in range(len(SearchBaiduProperty.lstTimeSlot) - 1):
                        self.flag = True
                        for j in range(15):
                            if self.flag:
                                url = SearchBaiduProperty.strUrlSearchPre.format(SearchBaiduProperty.lstTimeSlot[i],
                                                                                SearchBaiduProperty.lstTimeSlot[i + 1], searchkey,
                                                                                website, j * 50)
                                yield scrapy.Request(url=url, callback=self.parse)

        pass

    def parse(self, response):
        if not self.flag:
            pass
        self.judge(response)
        urls=titles=None
        try:
            urls=response.xpath('//div[@id="content_left"]/div[@id]/h3[@class="t"]/a/@href')
            titles=response.xpath('//div[@id="content_left"]/div[@id]/h3[@class="t"]/a')
        except:
            print('找不到该元素')
        if urls and titles:
            with open('./UrlTest.csv', 'a')as ofile:
                for i in range(len(urls)):
                    ofile.write(urls[i].root + ',' + self.strQ2B(titles[i].xpath('string(.)')[0].root) + ',' + self.current_website + "\n")

        pass

    def judge(self, response):
        ele = None
        try:
            ele = response.xpath('//div[@id="page"]/div/a[last()]//text()')[0].root
        except:
            print('找不到该元素')
        finally:
            if not ele or ele != '下一页 >':
                self.flag = False

    # 半角转全角
    def strQ2B(self, ustring):
        rstring = ""
        for uchar in ustring:
            if uchar == ',':
                uchar = '，'
            rstring += uchar
        return rstring