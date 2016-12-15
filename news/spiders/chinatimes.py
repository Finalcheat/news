# -*- coding: utf-8 -*-
import scrapy
import re
from news.items import NewsItem


class ChinatimesSpider(scrapy.Spider):
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
        htmlcontent = response.xpath('//div[contains(@class, "page_container")]/article/article').extract()[0]
        keywords = response.xpath('//div[@class="a_k"]/a/text()').extract()
        source = u'中時電子報'
        item = NewsItem(title=title, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item

