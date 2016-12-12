# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem


class EttodaySpider(scrapy.Spider):
    name = "ettoday"
    allowed_domains = ["ettoday.net"]
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
