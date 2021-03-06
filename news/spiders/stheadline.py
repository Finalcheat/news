# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from bs4 import BeautifulSoup
from news.items import NewsItem
from news.database import Database


class StheadlineSpider(scrapy.Spider):
    USE_PROXY = True
    name = "stheadline"
    allowed_domains = ["std.stheadline.com"]
    # start_urls = (
    #     "http://std.stheadline.com/daily/news-content.php?id=1526475&target=2",
    # )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("data-original") or attrs.get("src") or ""
        alt = attrs.get("alt", "")
        return {"src": src, "alt": alt}

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[contains(@class, "post-heading")]/h1/text()').extract()[0]
        pubtime = response.xpath('//div[contains(@class, "post-heading")]/div[@class="date"]').extract()[0]
        r = re.compile("(\d+)-(\d+)-(\d+) (\d+):(\d+)")
        r = re.findall(r, pubtime)
        if not r:
            r = re.compile("(\d+)-(\d+)-(\d+)")
            r = re.findall(r, pubtime)

        if not r:
            raise Exception(u"解析时间失败")
        r = [ int(x) for x in r[0] ]
        if len(r) == 5:
            pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4])
        else:
            pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        htmlcontent = response.xpath('//div[@class="post-content"]').extract()[0]

        soup = BeautifulSoup(htmlcontent, "lxml")
        for r in soup.find_all("a", class_="image"):
            r.name = "img"
            r["src"] = r["href"]
            r["alt"] = r["title"]
        htmlcontent = unicode(soup.body.contents[0])

        keywords = []
        source = u"星島日報"
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class StheadlineListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "stheadline_list"
    allowed_domains = ["std.stheadline.com"]
    start_urls = (
        "http://std.stheadline.com/daily/daily.php",           # 日报
    )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("data-original") or attrs.get("src") or ""
        alt = attrs.get("alt", "")
        return {"src": src, "alt": alt}

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        stheadline = StheadlineSpider()
        r = re.compile("^(http://std.stheadline.com/daily/)?news-content\.php\?id=\d+&target=\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = _href
                if not href.startswith("http"):
                    href = "http://std.stheadline.com/daily/" + href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, stheadline.parse)
