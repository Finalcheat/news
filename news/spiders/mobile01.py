# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class Mobile01Spider(scrapy.Spider):
    USE_PROXY = True
    name = "mobile01"
    allowed_domains = ["mobile01.com"]
    start_urls = (
        'http://www.mobile01.com/newsdetail/20115/final-fantasy-xv-15-rpg-act-review-series',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//header/h1[@class="topic"]/text()').extract()[0]
        pubtime = response.xpath('//div[@id="content"]/div[@id="section"]/div[@class="navbar"]/p[@class="nav"][last()]/text()').extract()[0]
        r = re.compile(u'(\d+)-(\d+)-(\d+) (\d+):(\d+)')
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4])
        htmlcontent = response.xpath('//div[@class="single-post"]/div[@class="single-post-content"]').extract()[0]
        keywords = []
        source = u'mobile01'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item
