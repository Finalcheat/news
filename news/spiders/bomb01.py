# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class Bomb01Spider(scrapy.Spider):
    USE_PROXY = True
    name = "bomb01"
    allowed_domains = ["bomb01.com"]
    # start_urls = (
    #     "http://www.bomb01.com/article/34896",
    # )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("src") or ""
        alt = attrs.get("alt", "")
        if src and not src.startswith("http"):
            src = "http://www.bomb01.com" + src
        return {"src": src, "alt": alt}

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@id="article"]/div/h1[@class="title"]/text()').extract()[0]
        pubtime = response.xpath('//div[contains(@class, "time")]').extract()[0]
        r = re.compile("(\d+)-(\d+)-(\d+)")
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u"解析时间失败")
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        htmlcontent = response.xpath('//div[@id="content"]').extract()[0]
        keywords = []
        source = u"boMb01"
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class Bomb01ListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "bomb01_list"
    allowed_domains = ["bomb01.com"]
    start_urls = (
        "https://www.bomb01.com/new/page/1/",
        "https://www.bomb01.com/new/page/2/",
        "https://www.bomb01.com/new/page/3/",
        "https://www.bomb01.com/new/page/4/",
        "https://www.bomb01.com/new/page/5/",
    )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("src") or ""
        alt = attrs.get("alt", "")
        if src and not src.startswith("http"):
            src = "http://www.bomb01.com" + src
        return {"src": src, "alt": alt}

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        bomb01 = Bomb01Spider()
        r = re.compile("^/article/\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "https://www.bomb01.com" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, bomb01.parse)
