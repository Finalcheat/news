# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from bs4 import BeautifulSoup
from news.items import NewsItem
from news.database import Database


class UdnStyleSpider(scrapy.Spider):
    USE_PROXY = True
    name = "udn_style"
    allowed_domains = ["style.udn.com"]
    # start_urls = (
    #     'http://style.udn.com/style/story/8067/1974324',
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h1[@class="story_art_title"]/font/text()').extract()[0]
        pubtime = response.xpath('//dl[@id="story-top"]/dd/text()').extract()[0]
        r = re.findall(u'(\d+)-(\d+)-(\d+)', pubtime)
        if not r:
            raise Exception(u'解析时间失败')
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        htmlcontent = response.xpath('//section[@id="story-main"]').extract()[0]
        keywords = response.xpath('//dl[contains(@class, "taglist")]/dd/a/text()').extract()
        source = u'udnSTYLE'
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class UdnStyleListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "udn_style_list"
    allowed_domains = ["style.udn.com"]
    start_urls = (
        "http://style.udn.com/style/index",
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        udn_style = UdnStyleSpider()
        r = re.compile("^/style/story/\d+/\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "http://style.udn.com" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=udn_style.parse)


class UdnSpider(scrapy.Spider):
    USE_PROXY = True
    name = "udn"
    allowed_domains = ["udn.com"]
    # start_urls = (
    #     "http://udn.com/news/story/9/2189655",
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h1[@id="story_art_title"]/text()').extract()[0]
        pubtime = response.xpath('//div[@id="story_bady_info"]/div[@class="story_bady_info_author"]/text()').extract()[0]
        r = re.compile(u"(\d+)-(\d+)-(\d+) (\d+):(\d+)")
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u"解析时间失败")
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4])
        htmlcontent = response.xpath('//div[@id="story_body_content"]').extract()[0]

        soup = BeautifulSoup(htmlcontent, "lxml")
        [h.extract() for h in soup.find_all("h1", id="story_art_title")]
        [d.extract() for d in soup.find_all("div", id="story_bar")]
        [d.extract() for d in soup.find_all("div", id="story_bady_info")]
        [a.extract() for a in soup.find_all("a", class_="photo_pop_icon")]
        [d.extract() for d in soup.find_all("div", class_="photo_pop")]
        htmlcontent = unicode(soup.body.contents[0])

        keywords = response.xpath('//div[@id="story_tags"]/a/text()').extract()
        source = u"聯合新聞網"
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class UdnListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "udn_list"
    allowed_domains = ["udn.com"]
    start_urls = (
        "http://udn.com/news/breaknews/1",         # 即时
        "http://udn.com/news/cate/2/6638",         # 要闻
        "http://udn.com/news/cate/2/7227",         # 运动
        "http://udn.com/news/cate/2/7225",         # 全球
        "http://udn.com/news/cate/2/6639",         # 社会
        "http://udn.com/news/cate/2/6644",         # 产经
        "http://udn.com/news/cate/2/6645",         # 股市
        "http://udn.com/news/cate/2/6649",         # 生活
        "http://udn.com/news/cindex/1012",         # 文教
        "http://udn.com/news/cate/2/6643",         # 评论
        "http://udn.com/news/cate/2/6641",         # 地方
        "http://udn.com/news/cate/2/6640",         # 两岸
        "http://udn.com/news/cate/2/7226",         # 数位
        "http://udn.com/news/cindex/1013",         # 旅游
        "http://udn.com/news/cindex/1014",         # 阅读
        "http://udn.com/news/cindex/1015",         # 杂志
    )

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        udn = UdnSpider()
        r = re.compile("^/news/story/\d+/\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "http://udn.com" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=udn.parse)
