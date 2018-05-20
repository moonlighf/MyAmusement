# -*- coding: utf-8 -*-
import scrapy
from DangDang.items import DangdangItem
from scrapy.http import Request
class DangdSpider(scrapy.Spider):
    name = 'DangD'
    allowed_domains = ['dangdang.com']
    '''
    
    '''
    start_urls = ['http://www.dangdang.com/']

    def parse(self, response):
        it = DangdangItem()
        it["title"] = response.xpath("//p[@class='name']/a[@name='itemlist-title']/text()").extract()
        it["Comment_Num"] = response.xpath("//p[@class='search_star_line']/a/text()").extract()
        it["price"] = response.xpath("//p[@class='price']/span[@class='search_now_price']/text()").extract()
        it["link"] = response.xpath("//p[@class='name']/a[@name='itemlist-title']/@href").extract()
        yield it
        for page in range(2, 51):
            url = 'http://category.dangdang.com/pg{}-cp01.54.06.00.00.00.html'.format(page)
            yield Request(url, callback=self.parse)
            break


