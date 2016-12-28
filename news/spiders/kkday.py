# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class KKdaySpider(scrapy.Spider):
    USE_PROXY = True
    name = "kkday"
    allowed_domains = ["blog.kkday.com"]
    # start_urls = (
    #     "http://blog.kkday.com/2016/12/10-london-must-eat.html",
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h3[contains(@class, "post-title")]/text()').extract()[0]
        title = title.replace("\n", "")
        pubtime = response.xpath('//abbr[@class="date-header"]/span/text()').extract()[0]
        r = re.compile(u"(\d+)年(\d+)月(\d+)日")
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u"解析时间失败")
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        htmlcontent = response.xpath('//div[contains(@class, "post-body")]').extract()[0]
        keywords = response.xpath('//span[@class="post-labels"]/a[@rel="tag"]/text()').extract()
        source = u"KKday"
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class KKdayListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "kkday_list"
    allowed_domains = ["blog.kkday.com"]
    start_urls = (
        "http://blog.kkday.com",
    )

    def parse(self, response):
        hrefs = response.xpath('//div[contains(@class, "post")]/h3[contains(@class, "post-title")]/a/@href').extract()
        kkday = KKdaySpider()
        for href in hrefs:
            if not Database.find_dup(href):
                yield scrapy.Request(href, callback=kkday.parse)
