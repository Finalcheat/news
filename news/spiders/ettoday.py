# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class EttodaySpider(scrapy.Spider):
    name = "ettoday"
    allowed_domains = ["www.ettoday.net"]
    start_urls = (
        # 'http://www.ettoday.net/',
        'http://www.ettoday.net/news/20161210/827108.htm',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//header/h2[contains(@class, "title")]/text()').extract()[0]
        pubtime = response.xpath('//span[@class="news-time"]/text()').extract()[0]
        r = re.findall(u'(\d+)年(\d+)月(\d+)日 (\d+):(\d+)', pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        htmlcontent = response.xpath('//div[@class="story"]').extract()[0]
        keywords = response.xpath('//div[@id="news-keywords"]/section/a/strong/text()').extract()
        source = u'Ettoday東森新聞雲'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class EttodayMoivesSpider(scrapy.Spider):
    USE_PROXY = True
    name = "ettoday_movies"
    allowed_domains = ["movies.ettoday.net"]
    # start_urls = (
    #     # "http://movies.ettoday.net/news/836200",
    #     "http://movies.ettoday.net/news/835783",
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h2[@class="title"]/text()').extract()[0]
        pubtime = response.xpath('//p[@class="date"]/text()').extract()[0]
        r = re.compile(u'(\d+)年(\d+)月(\d+)日 (\d+):(\d+)')
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4])
        htmlcontent = response.xpath('//div[@class="story"]').extract()[0]
        keywords = []
        source = u'ET看電影'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class EttodayMoivesListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "ettoday_movies_list"
    allowed_domains = ["movies.ettoday.net"]
    start_urls = (
        "http://movies.ettoday.net/news_list/384/1",             # 新闻
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        ettoday_moives = EttodayMoivesSpider()
        r = re.compile("^/news/\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "http://movies.ettoday.net" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=ettoday_moives.parse)


class EttodayTravelSpider(scrapy.Spider):
    USE_PROXY = True
    name = "ettoday_travel"
    allowed_domains = ["travel.ettoday.net"]
    # start_urls = (
    #     'http://travel.ettoday.net/article/829881.htm',
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@class="subjcet_news"]/h2[@class="title"]/text()').extract()[0]
        pubtime = response.xpath('//div[@class="subjcet_news"]/div[@class="date"]/text()').extract()[0]
        r = re.compile(u'(\d+)年(\d+)月(\d+)日 (\d+):(\d+)')
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4])
        htmlcontent = response.xpath('//div[@class="story"]').extract()[0]
        keywords = []
        source = u'ETtoday東森旅遊雲'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class EttodayTravelListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "ettoday_travel_list"
    allowed_domains = ["travel.ettoday.net"]
    start_urls = (
        "http://travel.ettoday.net/focus/%E6%96%B0%E8%81%9E%E7%84%A6%E9%BB%9E/",       # 新闻焦点
        "http://travel.ettoday.net/focus/%E6%9A%A2%E9%81%8A%E5%8F%B0%E7%81%A3/",       # 畅游台湾
        "http://travel.ettoday.net/focus/%E6%94%BE%E7%9C%BC%E6%B5%B7%E5%A4%96/",       # 放眼海外
        "http://travel.ettoday.net/focus/%E9%A3%AF%E5%BA%97%E6%97%85%E9%A4%A8/",       # 酒店旅馆
        "http://travel.ettoday.net/focus/%E4%BA%A4%E9%80%9A%E8%B3%87%E8%A8%8A/",       # 交通咨询
        "http://travel.ettoday.net/focus/%E7%BE%8E%E9%A3%9F%E5%9C%B0%E5%9C%96/",       # 美食地图
        "http://travel.ettoday.net/focus/%E5%84%AA%E6%83%A0%E5%BF%AB%E8%A8%8A/",       # 优惠快讯
        "http://travel.ettoday.net/focus/%E6%97%A5%E6%9C%AC%E6%97%85%E9%81%8A/",       # 日本旅游
        "http://travel.ettoday.net/focus/%E7%BE%8E%E9%A3%9F%E5%A5%BD%E5%BA%B7/",       # 美食好康
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        ettoday_travel = EttodayTravelSpider()
        r = re.compile("^http://travel\.ettoday\.net/article/\d+\.htm$")
        for href in hrefs:
            if r.match(href) and not Database.find_dup(href):
                yield scrapy.Request(href, ettoday_travel.parse)


class EttodaySportsSpider(scrapy.Spider):
    name = "ettoday_sports"
    allowed_domains = ["sports.ettoday.net"]
    start_urls = (
        'http://sports.ettoday.net/news/829873',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h1[@class="title"]/text()').extract()[0]
        pubtime = response.xpath('//div[@class="date"]/text()').extract()[0]
        r = re.compile(u'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)')
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        htmlcontent = response.xpath('//div[@class="story"]').extract()[0]
        keywords = []
        source = u'ET運動雲'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item
