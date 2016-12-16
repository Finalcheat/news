# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem


class BeautiesSpider(scrapy.Spider):
    name = "beauties"
    allowed_domains = ["beauties.life"]
    start_urls = (
        'http://beauties.life/?p=7141',
    )

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@class="post_title_wrapper"]/h1[contains(@class, "entry_title")]/text()').extract()[0]
        htmlcontent = response.xpath('//div[contains(@class, "blog_post_content")]/div[@itemprop="articleBody"]').extract()[0]
        keywords = []
        source = u'BOL美麗日報'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item
