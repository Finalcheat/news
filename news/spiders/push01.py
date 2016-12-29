# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class Push01Spider(scrapy.Spider):
    USE_PROXY = True
    name = "push01"
    allowed_domains = ["push01.net"]
    # start_urls = (
    #     "http://www.push01.net/post/420795",
    # )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("src") or ""
        alt = attrs.get("alt", "")
        if src and not src.startswith("http"):
            src = "http://www.push01.net" + src
        return {"src": src, "alt": alt}

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[contains(@class, "content")]/h1[@itemprop="headline"]/a/text()').extract()[0]
        pubtime = response.xpath('//div[contains(@class, "description")]/p[@class="date"]').extract()[0]
        r = re.compile("(\d+)-(\d+)-(\d+)")
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u"解析时间失败")
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        htmlcontent = response.xpath('//div[contains(@class, "postContent")]').extract()[0]
        keywords = []
        source = u"PUSH01"
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class Push01ListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "push01_list"
    allowed_domains = ["push01.net"]
    start_urls = (
        "http://www.push01.net",
    )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("src") or ""
        alt = attrs.get("alt", "")
        if src and not src.startswith("http"):
            src = "http://www.push01.net" + src
        return {"src": src, "alt": alt}

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        push01 = Push01Spider()
        r = re.compile("^/post/\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "http://www.push01.net" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, push01.parse)
