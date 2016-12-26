# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class LetsgojpSpider(scrapy.Spider):
    USE_PROXY = True
    name = "letsgojp"
    allowed_domains = ["letsgojp.com"]
    # start_urls = (
    #     'http://kyushu.letsgojp.com/archives/23471/',
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h1[@class="post-title"]/text()').extract()[0]
        pubtime = response.xpath('//div[@id="postContent"]/div[@class="row"]/div/text()').extract()[0]
        r = re.compile(u'(\d+)年(\d+)月(\d+)日')
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        htmlcontent = response.xpath('//div[@id="postContent"]/div[@id="content"]').extract()[0]
        keywords = []
        source = u'日本樂吃購'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class LetsgojpListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "letsgojp_list"
    allowed_domains = ["letsgojp.com"]
    start_urls = (
        "http://okinawa.letsgojp.com/",               # 冲绳
        "http://hokkaido.letsgojp.com/",              # 北海道
        "http://tohoku.letsgojp.com/",                # 东北
        "http://tokyo.letsgojp.com/",                 # 东京
        "http://hokuriku.letsgojp.com/",              # 北陆
        "http://kyoto.letsgojp.com/",                 # 京东
        "http://nara.letsgojp.com/",                  # 奈良
        "http://kobe.letsgojp.com/",                  # 神户
        "http://osaka.letsgojp.com/",                 # 大阪
        "http://wakayama.letsgojp.com/",              # 和歌山
        "http://kyushu.letsgojp.com/",                # 九州
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        letsgojp = LetsgojpSpider()
        r = re.compile("http://.*letsgojp\.com/archives/\d+/$")
        for href in hrefs:
            if r.match(href) and not Database.find_dup(href):
                yield scrapy.Request(href, letsgojp.parse)
