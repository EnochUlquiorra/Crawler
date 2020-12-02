import scrapy
from WendaSpider.property import SearchBingProperty
from selenium import webdriver
import json,time

#pc端

class Searchurlbdzd(scrapy.Spider):
    name = 'searchurlbdzd'
    #allowed_domains = ['cn.bing.com']
    #start_urls = ['https://cn.bing.com/search?q=税+site%3azhidao.baidu.com&first=31']
    
    def start_requests(self):

        driver = webdriver.Chrome()
        driver.get('https://baidu.com/')

        #driver.find_element_by_xpath('//*[@id="u1"]/a[7]').click()
        login=driver.find_elements_by_css_selector('#u1>a.lb')[0]
        login.click()

        time.sleep(2)
        #driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__footerULoginBtn"]').click()

        namelogin=driver.find_elements_by_css_selector('p.tang-pass-footerBarULogin')[0]
        namelogin.click()
        time.sleep(3)

        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__userName"]').send_keys('****')
        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__password"]').send_keys('****')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_11__submit"]').click()

        time.sleep(30)

        cookies = driver.get_cookies()
        f1 = open('cookie.txt','w')
        f1.write(json.dumps(cookies))
        f1.close()


        for i in range(1,20):
            #url = 'https://zhidao.baidu.com/list?category=%E6%95%99%E8%82%B2%E5%9F%B9%E8%AE%AD&pn='+str(i*40)+'&fr=daohang'                                                            
            #yield scrapy.Request(url=url, cookies=self.cookie, callback=self.parse)
            url = 'https://zhidao.baidu.com/list?category=%E6%95%99%E8%82%B2%E5%9F%B9%E8%AE%AD&rn=40&pn='+str(i*40)+'&ie=utf8&_pjax=%23j-question-list-pjax-container'
            yield scrapy.Request(url=url, callback=self.parse)
        pass
    

    def parse(self, response):

        titles = None
        #urls = titles = None
        try:
            titles = response.xpath('//div[@class="question-tags"]/a')
            #urls = response.xpath('//div[@class="question-title-section"]/div[@class="question-title"]/a/@href')
            #titles = response.xpath('//div[@class="question-title-section"]/div[@class="question-title"]/a')
        except:
            print('找不到该元素')
        if titles :
            with open('./Url_baiduzhidao.csv', 'a',encoding="utf-8")as ofile:
                for i in range(len(titles)):
                    strTitle=self.strQ2B(titles[i].xpath('string(.)')[0].root)
                    ofile.write(strTitle)
                    #strTitle=self.strQ2B(titles[i].xpath('string(.)')[0].root)
                    #if strTitle.find('教育')>=0:
                    #ofile.write(strUrl + ',' + strTitle + ',' + self.current_website + "\n")

        pass

               
    # 半角转全角
    def strQ2B(self, ustring):
        rstring = ""
        for uchar in ustring:
            if uchar == ',':
                uchar = '，'
            rstring += uchar
        return rstring
