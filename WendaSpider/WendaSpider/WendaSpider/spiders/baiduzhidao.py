import scrapy
import re

#移动端
class BaiduzhidaoSpider(scrapy.Spider):
    name = 'baiduzhidao'
    allowed_domains = ['zhidao.baidu.com']

    timestamp='2017-11-01'

    def start_requests(self):
        with open('Url_baiduzhidao_23.csv', 'r',encoding='UTF-8')as ifile:
            for line in ifile:
                item = line.split(',')
                url = item[0]
                yield scrapy.Request(url, self.parse)
        pass

    def parse(self, response):
        timestamp = None
        try:
            timestamp = self.strDeal(response.xpath('//p[@class="question-author-meta"]/text()[last()]')[0].root)
        except:
            print("该问题没有答案")
        if timestamp:
            self.timestamp=timestamp
        else:
            timestamp=self.timestamp


        title = self.strDeal(response.xpath('string(//div[@class="wgt-question-title"])')[0].root)
        descriptions = self.strDeal(response.xpath('string(//div[@class="wgt-question-desc-inner"])')[0].root)
        if len(descriptions)==0:
            question=title
        else:
            question=title+'\n'+descriptions

        answerAll = response.xpath('//div[@class="clear w-detail-content"]/div')
        answerInner = answerAll.xpath('./p')
        if len(answerInner) == 0:
            answerPre = answerAll
        else:
            answerPre = answerInner
        answer = ''
        for line in answerPre:
            strLine = self.strDeal(line.xpath('string(.)')[0].root)
            if len(strLine) != 0 and not re.search(r'\d\d:\d\d', strLine):
                answer = answer + strLine + '\n'
        if len(answer) == 0:
            answer += '\n'

        with open('./BaiduZhidao23.txt', 'a', encoding='utf-8')as ofile:
            ofile.write('D:' + timestamp + '\n')
            ofile.write('Q:' + question + '\n')
            ofile.write('A1:' + answer + '\n')
        pass

    def strDeal(self, ustring):
        s = ustring.replace(' ', '').replace('\n', '').replace('\r', '')
        return s

