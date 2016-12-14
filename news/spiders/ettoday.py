# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem


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
    name = "ettoday_moives"
    allowed_domains = ["movies.ettoday.net"]
    start_urls = (
        'http://movies.ettoday.net/news/829812',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h2[@class="title"]/text()').extract()[0]
        pubtime = response.xpath('//p[@class="date"]/text()').extract()[0]
        r = re.compile(u'(\d+)年(\d+)月(\d+)日 (\d+):(\d+)')
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        htmlcontent = response.xpath('//div[@class="story"]').extract()[0]
        keywords = []
        source = u'ET看電影'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class EttodayTravelSpider(scrapy.Spider):
    name = "ettoday_travel"
    allowed_domains = ["travel.ettoday.net"]
    start_urls = (
        'http://travel.ettoday.net/article/829881.htm',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@class="subjcet_news"]/h2[@class="title"]/text()').extract()[0]
        pubtime = response.xpath('//div[@class="subjcet_news"]/div[@class="date"]/text()').extract()[0]
        r = re.compile(u'(\d+)年(\d+)月(\d+)日 (\d+):(\d+)')
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        htmlcontent = response.xpath('//div[@class="story"]').extract()[0]
        keywords = []
        source = u'ETtoday東森旅遊雲'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


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
