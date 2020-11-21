import scrapy
from WendaSpider.property import Wenda360Property

#移动端
class Wenda360Spider(scrapy.Spider):
    name = 'wenda360'
    allowed_domains = ['wenda.so.com']
    # start_urls=['https://wenda.so.com/q/1387556652064124']

    def start_requests(self):

        with open('Url_360.csv', 'r')as ifile:
            for line in ifile:
                item=line.split(',')
                url = item[0]
                yield scrapy.Request(url, self.parse)
        pass

    def parse(self, response):
        timestamp = self.strDeal(response.xpath('//*[@id="ask"]/div[2]/span[2]/text()')[0].root)

        title = self.strDeal(response.xpath('string(//div[@class="ask-title"])')[0].root)
        descriptions = self.strDeal(response.xpath('string(//div[@class="mt10 ask-content src-import"])')[0].root)
        if len(descriptions) == 0:
            question = title
        else:
            question = title + '\n' + descriptions

        answerAll = response.xpath('//div[@class="ans-box-con src-import"]')
        answerInner = answerAll.xpath('./p')
        if len(answerInner) == 0:
            answerPre = answerAll
        else:
            answerPre = answerInner
        answer = ''
        for line in answerPre:
            strLine = self.strDeal(line.xpath('string(.)')[0].root)
            if len(strLine) != 0:
                answer = answer + strLine + '\n'
        if len(answer) == 0:
            answer += '\n'

        with open('./360Wenda.txt', 'a')as ofile:
            if len(answer)!=0 and len(question)!=0 and len(timestamp)!=0:
                ofile.write('D:' + timestamp + '\n')
                ofile.write('Q:' + question + '\n')
                ofile.write('A1:' + answer + '\n')

        pass


    def strDeal(self, ustring):
        s = ustring.replace(' ', '').replace('\n\n', '')
        return s
