# -*- coding: utf-8 -*-
import scrapy
from aiwanCrawl.settings import SITE_URL
from aiwanCrawl.items import AiwancrawlItem
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule


class AiwanSpider(RedisCrawlSpider):
    name = 'aiwan'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']

    rules = (
        Rule(LinkExtractor(
            allow=r'/vod-type-id-1-type--area--year--star--state--order-addtime-p-\d+\.html'),
             callback='parse_item', follow=True),
    )
    redis_key = 'aiwan'

    def parse_item(self, response):
        li_list = response.xpath('//*[@id="contentList"]/ul/li')
        for li in li_list:
            item = AiwancrawlItem()
            item['title'] = li.xpath(
                './div[2]//span[1]/a/@title').extract_first()
            item['play_times'] = li.xpath(
                './div[2]//span[3]/text()').extract_first()
            url = SITE_URL + li.xpath(
                './div[2]//span[1]/a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_url,
                                 meta={'item': item})

    def parse_url(self, response):
        item = response.meta['item']
        item['role'] = response.xpath(
            "//div[@class='txt_intro_con']/ul/li[1]/a[1]/text()").extract_first()
        item['director'] = response.xpath(
            "//div[@class='txt_intro_con']/ul/li[2]/em[2]/a/text()").extract_first()
        item['introduction'] = response.xpath(
            "//div[@class='txt_intro_con']/ul//li[3]/p/span[1]/text()").extract_first()
        yield item
