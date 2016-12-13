# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem


class UdnStyleSpider(scrapy.Spider):
    name = "udn_style"
    allowed_domains = ["style.udn.com"]
    start_urls = (
        'http://style.udn.com/style/story/8067/1974324',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h1[@class="story_art_title"]/font/text()').extract()[0]
        pubtime = response.xpath('//dl[@id="story-top"]/dd/text()').extract()[0]
        r = re.findall(u'(\d+)-(\d+)-(\d+)', pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        htmlcontent = response.xpath('//section[@id="story-main"]').extract()[0]
        keywords = response.xpath('//dl[contains(@class, "taglist")]/dd/a/text()').extract()[0]
        source = u'udnSTYLE'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class UdnSpider(scrapy.Spider):
    name = "udn"
    allowed_domains = ["udn.com"]
    start_urls = (
        'http://www.udn.com/',
    )

    def parse(self, response):
        pass
