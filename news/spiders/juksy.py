# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem


class JuksySpider(scrapy.Spider):
    name = "juksy"
    allowed_domains = ["juksy.com"]
    start_urls = (
        'https://www.juksy.com/archives/60520',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@id="articleHead/h1/text()"]').extract()[0]
        pubtime = response.xpath('//div[@id="date"]/text()').extract()[0]
        r = re.findall(u'(\d+)-(\d+)-(\d+)', pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        htmlcontent = response.xpath('//div[@id="articleMain"]').extract()[0]
        keywords = response.xpath('//div[@id="mainLeftWrap"]/article/h2/a/text()').extract()
        source = u'流行生活網'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item
