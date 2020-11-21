import scrapy

#pc端（搜狗访问多了的话会被禁ip，需要准备代理ip池，每次随机选择一个ip访问，这个我没写）
class SougouwenwenSpider(scrapy.Spider):
    name = 'sougouwenwen'
    #allowed_domains = ['https://wenwen.sogou.com/']
    allowed_domains = ['wenwen.sougou.com']
    #start_urls=['https://wenwen.sogou.com/z/q829377877.htm']

    def start_requests(self):
        with open('./Url_sougou_67copy.csv', 'r',encoding='utf-8') as ifile:
            for line in ifile:
                item = line.split(',')
                url = item[0]
                yield scrapy.Request(url, self.parse)
        pass

    def parse(self, response):
        timestamp = response.xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]//text()')[0].root.split(' ')[0]
        title = response.xpath('//*[@id="question_title_val"]//text()')[0].root
        descriptions = response.xpath('string(//pre[@class="detail-tit-info"])')[0].root
        if len(descriptions) == 0:
            question = title
        else:
            question = title + '\n' + descriptions
        answerSe = response.xpath('//pre[@class="replay-info-txt answer_con"]')
        with open('./SougouWenwen.txt', 'a', encoding='utf-8') as ofile:
            
            ofile.write('D:' + timestamp + '\n')
            ofile.write('Q:' + question + '\n')
            
            i = 0
            for answers in answerSe:
                i += 1
                strA = ""
                for answer in answers.xpath('string(.)'):
                    strA += answer.root
                ofile.write('A' + str(i) + ':' + self.strDeal(strA) + '\n')
            ofile.write('\n')

        pass

    def strDeal(self, ustring):
        s = ustring.replace(' ', '').replace('\n\n', '\n')
        return s