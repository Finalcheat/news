# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem


class SetnSpider(scrapy.Spider):
    name = "setn"
    allowed_domains = ["setn.com"]
    start_urls = (
        'http://www.setn.com/News.aspx?NewsID=206790',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@class="title"]/h1/text()').extract()[0]
        pubtime = response.xpath('//span[@class="date"]/text()').extract()[0]
        r = re.findall(u'(\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)', pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        htmlcontent = response.xpath('//div[@id="ckuse"]').extract()[0]
        keywords = response.xpath('//div[contains(@class, "keyword")]/ul/li/a/strong/text()').extract()
        source = u'SET三立新聞網'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item
