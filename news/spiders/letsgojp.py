# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem


class LetsgojpSpider(scrapy.Spider):
    name = "letsgojp"
    allowed_domains = ["letsgojp.com"]
    start_urls = (
        'http://kyushu.letsgojp.com/archives/23471/',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h1[@class="post-title"]/text()').extract()[0]
        pubtime = response.xpath('//div[@id="postContent"]/div[@class="row"]/div/text()').extract()[0]
        r = re.compile(u'(\d+)年(\d+)月(\d+)日')
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        htmlcontent = response.xpath('//div[@id="postContent"]/div[@id="content"]').extract()[0]
        print htmlcontent
        keywords = []
        source = u'日本樂吃購'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item
