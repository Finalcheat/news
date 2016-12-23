# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class JuksySpider(scrapy.Spider):
    USE_PROXY = True
    name = "juksy"
    allowed_domains = ["juksy.com"]
    # start_urls = (
    #     'https://www.juksy.com/archives/60520',
    # )

    def img_callback(self, pipeline, attrs):
        data_src = attrs.get("data-src") or attrs.get("src") or ""
        alt = attrs.get("alt", "")
        if data_src and not data_src.startswith("http"):
            data_src = "https://static.juksy.com" + data_src
        return {"src": data_src, "alt": alt}

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@id="articleHead"]/h1/text()').extract()[0]
        pubtime = response.xpath('//div[@id="date"]/text()').extract()[0]
        r = re.findall(u'(\d+)\.(\d+)\.(\d+)', pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        htmlcontent = response.xpath('//div[@id="articleMain"]').extract()[0]
        keywords = response.xpath('//div[@id="mainLeftWrap"]/article/h2/a/text()').extract()
        source = u'流行生活網'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class JuksyListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "juksy_list"
    allowed_domains = ["juksy.com"]
    start_urls = (
        "https://www.juksy.com/channel/latest",
    )

    def img_callback(self, pipeline, attrs):
        data_src = attrs.get("data-src") or attrs.get("src") or ""
        alt = attrs.get("alt", "")
        if data_src and not data_src.startswith("http"):
            data_src = "https://static.juksy.com" + data_src
        return {"src": data_src, "alt": alt}

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        juksy = JuksySpider()
        r = re.compile("^/archives/\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "https://www.juksy.com" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=juksy.parse)
