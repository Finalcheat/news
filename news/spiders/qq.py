# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem


class QqSpider(scrapy.Spider):
    name = "qq"
    allowed_domains = ["qq.com"]
    start_urls = (
        'http://news.qq.com/a/20161218/009311.htm',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@class="qq_article"]/div/h1/text()').extract()[0]
        pubtime = response.xpath('//div[@class="qq_article"]/div/div/div[@class="a_Info"]/span[@class="a_time"]/text()').extract()[0]
        pubtime = datetime.datetime.strptime(pubtime, "%Y-%m-%d %H:%M")
        htmlcontent = response.xpath('//div[@id="Cnt-Main-Article-QQ"]').extract()[0]
        source = u"腾讯新闻"
        keywords = []
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class QqListSpider(scrapy.Spider):
    name = "qq_list"
    allowed_domains = ["qq.com"]
    start_urls = (
        "http://news.qq.com/",
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        qq = QqSpider()
        r = re.compile("^http://news\.qq\.com/a/\d+/\d+\.htm$")
        for href in hrefs:
            if r.match(href):
                # print href
                yield scrapy.Request(href, callback=qq.parse)
