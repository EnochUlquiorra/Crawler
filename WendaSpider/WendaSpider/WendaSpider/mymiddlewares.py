from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.http import HtmlResponse
from scrapy import signals
import random
import pyppeteer
import asyncio
import os 

pyppeteer.DEBUG = False 
 
class FundscrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self) :
        
        self.timeout = 50
        self.browse_num = 0

        print("Init downloaderMiddleware use pypputeer.")
        os.environ['PYPPETEER_CHROMIUM_REVISION'] ='588429'
        # pyppeteer.DEBUG = False
        print(os.environ.get('PYPPETEER_CHROMIUM_REVISION'))
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.getbrowser())
        loop.run_until_complete(task)
 
        #self.browser = task.result()
        print(self.browser)
        print(self.page)
        # self.page = await browser.newPage()

    async def getbrowser(self):
        # 通过设置user-agent，用来模拟移动设备
        # user_ag = 'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; ' + 'CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
        # options.add_argument('user-agent=%s' % user_ag)
        options ={
            'headless':True,
        }
        self.browser = await pyppeteer.launch(options, ignoreDefaultArgs=['--enable-automation'])    #打开浏览器
        #self.browser = await pyppeteer.launch() 
        self.page = await self.browser.newPage()    
        await self.page.setViewport({
        "width": 1000,
        "height": 1000
        })
        await self.page.setUserAgent('MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; ' + 'CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
        # return await pyppeteer.launch()
    
    async def getnewpage(self): 
        return  await self.browser.newPage()
 
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
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.usePypuppeteer(request))
        loop.run_until_complete(task)  
        
        return HtmlResponse(url=request.url, body=task.result(), encoding="utf-8",request=request)
 
    async def usePypuppeteer(self, request):
        print(request.url)
        # page = await self.browser.newPage()
        await self.page.goto(
            request.url,
            options = {
                'timeout':300,
            }
        )
        content = await self.page.content()
        return content 
 
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

    def spider_closed(self):
            # 爬虫结束 关闭窗口
        self.browser.close()
        pass


class TooManyRequestsRetryMiddleware(RetryMiddleware):
    
    def __init__(self, crawler):
        super(TooManyRequestsRetryMiddleware, self).__init__(crawler.settings)
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if response.status == 418:
            self.crawler.engine.pause()
            time.sleep(60)  # If the rate limit is renewed in a minute, put 60 seconds, and so on.
            self.crawler.engine.unpause()
            return request

        return response