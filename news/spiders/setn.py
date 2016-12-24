# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class SetnSpider(scrapy.Spider):
    USE_PROXY = True
    name = "setn"
    allowed_domains = ["setn.com"]
    # start_urls = (
    #     "http://www.setn.com/News.aspx?NewsID=210260",
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@class="title"]/h1/text()').extract()[0]
        pubtime = response.xpath('//span[@class="date"]/text()').extract()[0]
        r = re.compile("(\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)")
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4], second=r[5])
        htmlcontent = response.xpath('//div[@id="ckuse"]').extract()[0]
        keywords = response.xpath('//div[contains(@class, "keyword")]/ul/li/a/strong/text()').extract()
        source = u'SET三立新聞網'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class SetnListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "setn_list"
    allowed_domains = ["setn.com"]
    start_urls = (
        "http://www.setn.com/ViewAll.aspx",
        "http://www.setn.com/ViewAll.aspx?p=2",
        "http://www.setn.com/ViewAll.aspx?p=3",
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        setn = SetnSpider()
        r = re.compile("^/News\.aspx\?NewsID=\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "http://www.setn.com" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=setn.parse)



class SetnESpider(scrapy.Spider):
    USE_PROXY = True
    name = "setn_e"
    allowed_domains = ["setn.com"]
    # start_urls = (
    #     "http://www.setn.com/E/News.aspx?NewsID=210255",
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h1[@id="newsTitle"]/text()').extract()[0]
        pubtime = response.xpath('//div[@class="titleBtnBlock"]/div[@class="time"]/text()').extract()[0]
        r = re.compile("(\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)")
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u"解析时间失败")
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4], second=r[5])
        htmlcontent = response.xpath('//div[@id="ckuse"]').extract()[0]
        keywords = response.xpath('//div[contains(@class, "keyword")]/ul/li/a/strong/text()').extract()
        source = u"娛樂星聞"
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class SetnEListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "setn_e_list"
    allowed_domains = ["setn.com"]
    start_urls = (
        "http://www.setn.com/E/ViewAll.aspx",
        "http://www.setn.com/E/ViewAll.aspx?p=2",
        "http://www.setn.com/E/ViewAll.aspx?p=3",
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        setn_e = SetnESpider()
        r = re.compile("^news\.aspx\?newsid=\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "http://www.setn.com/E/" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=setn_e.parse)
