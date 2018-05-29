import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import base64
from scrapy_splash import SplashRequest


class KeyholeSpider(CrawlSpider):

    name = 'keyhole'

    def start_requests(self):
        allowed_domains = ['keyhole.co']
        url = 'http://keyhole.co/'

        #LUA Script
        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            local button = splash:select('button')
            button:mouse_click()
            splash:wait(0.1)
            return splash:html()
        end
        """
        
        yield SplashRequest(url, self.parse_result, endpoint='execute',
                            args={'lua_source': script})
        

    def parse_result(self, response):
        doc_title = response.body_as_unicode()
        # ...