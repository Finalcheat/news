# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from news.items import NewsItem
from news.database import Database


class CdnewsSpider(scrapy.Spider):
    USE_PROXY = True
    name = "cdnews"
    allowed_domains = ["cdnews.com.tw"]
    # start_urls = (
    #     "http://www.cdnews.com.tw/cdnews_site/docDetail.jsp?coluid=121&docid=103983004",
    # )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("src") or ""
        alt = attrs.get("alt", "")
        if src and not src.startswith("http"):
            src = "http://www.cdnews.com.tw" + src
        return {"src": src, "alt": alt}

    def parse(self, response):
        href = response.url
        title = response.xpath('//div[@class="content_title"]/h2/text()').extract()[0]
        pubtime = response.xpath('//div[@class="content_title"]/h6/text()').extract()[0]
        r = re.compile("(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)")
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u"解析时间失败")
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        htmlcontent = response.xpath('//div[@id="docbody"]').extract()[0]
        keywords = []
        source = u"中央網路報"
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class CdnewsListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "cdnews_list"
    allowed_domains = ["cdnews.com.tw"]
    start_urls = (
        "http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=127",       # 政党要闻
        "http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=118",       # 展销会讯
        "http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=119",       # 投资法规
        "http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=120",       # 两岸房市
        "http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=121",       # 教育艺文
        "http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=123",       # 出门看天
        "http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=124",       # 走遍台湾
        "http://www.cdnews.com.tw/cdnews_site/coluOutline.jsp?coluid=125",       # 逍遥神州
    )

    def img_callback(self, pipeline, attrs):
        src = attrs.get("src") or ""
        alt = attrs.get("alt", "")
        if src and not src.startswith("http"):
            src = "http://www.cdnews.com.tw" + src
        return {"src": src, "alt": alt}

    def parse(self, response):
        hrefs = response.xpath('//a/@href').extract()
        cdnews = CdnewsSpider()
        r = re.compile("^docDetail\.jsp\?coluid=\d+&docid=\d+$")
        for _href in hrefs:
            if r.match(_href):
                href = "http://www.cdnews.com.tw/cdnews_site/" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=cdnews.parse)
