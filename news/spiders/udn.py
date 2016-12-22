# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class UdnStyleSpider(scrapy.Spider):
    USE_PROXY = True
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
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        htmlcontent = response.xpath('//section[@id="story-main"]').extract()[0]
        keywords = response.xpath('//dl[contains(@class, "taglist")]/dd/a/text()').extract()
        source = u'udnSTYLE'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class UdnStyleListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "udn_style_list"
    allowed_domains = ["style.udn.com"]
    start_urls = (
        "http://style.udn.com/style/index",
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        udn_style = UdnStyleSpider()
        r = re.compile("^/style/story/\d+/\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "http://style.udn.com" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=udn_style.parse)
