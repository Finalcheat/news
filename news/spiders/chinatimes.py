# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class ChinatimesSpider(scrapy.Spider):
    USE_PROXY = True
    name = "chinatimes"
    allowed_domains = ["chinatimes.com"]
    start_urls = (
        'http://www.chinatimes.com/realtimenews/20161215002455-260404',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//header/h1/text()').extract()[0]
        pubtime = response.xpath('//div[@class="reporter"]/time/text()').extract()[0]
        r = re.findall(u'(\d+)年(\d+)月(\d+)日 (\d+):(\d+)', pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4])
        htmlcontent = response.xpath('//div[contains(@class, "page_container")]/article/article').extract()[0]
        keywords = response.xpath('//div[@class="a_k"]/a/text()').extract()
        source = u'中時電子報'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class ChinatimesListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "chinatimes_list"
    allowed_domains = ["chinatimes.com"]
    start_urls = (
        "http://www.chinatimes.com/realtimenews/",
        "http://www.chinatimes.com/realtimenews/?page=2",
        "http://www.chinatimes.com/realtimenews/?page=3",
        "http://www.chinatimes.com/politic/",
        "http://www.chinatimes.com/life/",
        "http://www.chinatimes.com/society/",
        "http://www.chinatimes.com/money/",
        "http://www.chinatimes.com/world",
        "http://www.chinatimes.com/chinese",
        "http://www.chinatimes.com/armament",
        "http://www.chinatimes.com/star/",
        "http://www.chinatimes.com/sports/",
        "http://www.chinatimes.com/newspapers",
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        chinatimes = ChinatimesSpider()
        r = re.compile("/(realtimenews|newspapers)/\d+-\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "http://www.chinatimes.com" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=chinatimes.parse)
