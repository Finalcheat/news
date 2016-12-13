# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem


class Mobile01Spider(scrapy.Spider):
    name = "mobile01"
    allowed_domains = ["mobile01.com"]
    start_urls = (
        'http://www.mobile01.com/newsdetail/20115/final-fantasy-xv-15-rpg-act-review-series',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//header/h1[@class="topic"]/text').extract()[0]
        pubtime = response.xpath('//div[@id="content"]/div[@id="section"]/div[@class="navbar"]/p[@class="nav"]/text()').extract()[0]
        r = re.compile(u'(\d+)-(\d+)-(\d+) (\d+):(\d+)')
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        htmlcontent = response.xpath('//div[@class="single-post"]/div[@class="single-post-content"]').extract()[0]
        keywords = []
        source = u'mobile01'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item
