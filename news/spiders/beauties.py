# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class BeautiesSpider(scrapy.Spider):
    USE_PROXY = True
    name = "beauties"
    allowed_domains = ["beauties.life"]
    # start_urls = (
    #     'http://beauties.life/?p=7141',
    # )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("data-src") or attrs.get("src") or ""
        alt = attrs.get("alt", "")
        return {"src": src, "alt": alt}

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@class="post_title_wrapper"]/h1[contains(@class, "entry-title")]/text()').extract()[0]
        htmlcontent = response.xpath('//div[contains(@class, "blog_post_content")]/div[@itemprop="articleBody"]').extract()[0]
        pubtime = datetime.datetime.now()
        keywords = []
        source = u'BOL美麗日報'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class BeautiesListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "beauties_list"
    allowed_domains = ["beauties.life"]
    start_urls = (
        "http://beauties.life/",
        "http://beauties.life/?cat=1",             # 生活
        "http://beauties.life/?cat=3",             # 新闻
        "http://beauties.life/?cat=4",             # 娱乐
        "http://beauties.life/?cat=5",             # 惊奇
        "http://beauties.life/?cat=2514",          # 女性
        "http://beauties.life/?cat=6",             # 动物
        "http://beauties.life/?cat=3086",          # 世界
    )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("data-src") or attrs.get("src") or ""
        alt = attrs.get("alt", "")
        return {"src": src, "alt": alt}

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        beauties = BeautiesSpider()
        r = re.compile("^http://beauties\.life/\?p=\d+$")
        for href in hrefs:
            if r.match(href) and not Database.find_dup(href):
                yield scrapy.Request(href, beauties.parse)
