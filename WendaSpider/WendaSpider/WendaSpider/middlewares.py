# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import urllib3
from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.support import wait


class WendaspiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WendaspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities, ActionChains

import time
from scrapy.http import HtmlResponse


class SeleniumMiddleware(object):
    def __init__(self):
        self.timeout = 50

        self.browse_num = 0
        # 2.Firefox---------------------------------
        # 实例化参数对象
        options = webdriver.ChromeOptions()
        options.binary_location=r'C:\Users\admin\AppData\Local\Google\Chrome\Application\chrome.exe'
        ## 无界面
        #options.add_argument('--headless')
        # 关闭浏览器弹窗
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2
            }
        }
        options.add_experimental_option('prefs', prefs)

        #不加载图片
        options.add_argument('blink-settings=imagesEnabled=false')

        # 通过设置user-agent，用来模拟移动设备
        #user_ag = 'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; ' + 'CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
        user_ag = "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)"
        #user_ag = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        options.add_argument('user-agent=%s' % user_ag)

        # 打开浏览器
        self.browser = webdriver.Chrome(chrome_options=options)
        # 指定浏览器窗口大小
        self.browser.set_window_size(1400, 1800)
        # 设置页面加载超时时间
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def process_request(self, request, spider, urllib2=None):

        #定时清除浏览器缓存，否则爬取速度越来越慢
        if self.browse_num >= 40:
            send_command = ('POST', '/session/$sessionId/chromium/send_command')
            self.browser.command_executor._commands['SEND_COMMAND'] = send_command
            self.browser.execute('SEND_COMMAND', dict(cmd='Network.clearBrowserCache', params={}))
            self.browser.delete_all_cookies()
            self.browse_num = 0


        # 当请求的页面不是当前页面时
        if self.browser.current_url != request.url:
            # 获取页面
            self.browser.get(request.url)
            # time.sleep(2)
            self.browse_num += 1


        # 搜狗问答多个答案时点开隐藏
        if request.url.startswith("https://www.sogou.com/"):
            try:
                a = self.browser.find_element_by_xpath('//*[@id="container"]/div/div[2]/div[2]/div[2]/a')
                a.click()
                time.sleep(2)
            except JavascriptException as e:
                pass
            except Exception as e:
                pass
        else:
            pass
        # 返回页面的response
        return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source,
                            encoding="utf-8", request=request)

    def spider_closed(self):
        # 爬虫结束 关闭窗口
        self.browser.close()
        pass

    @classmethod
    def from_crawler(cls, crawler):
        # 设置爬虫结束的回调监听
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s
