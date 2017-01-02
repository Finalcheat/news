# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from bs4 import BeautifulSoup
from news.items import NewsItem
from news.database import Database


class AppledailySpider(scrapy.Spider):
    USE_PROXY = True
    name = "appledaily"
    allowed_domains = ["appledaily.com.tw"]
    # start_urls = (
    #     "http://www.appledaily.com.tw/realtimenews/article/local/20160930/958539/",      # 视频
    #     "http://www.appledaily.com.tw/realtimenews/article/3c/20160829/937956/",         # 图片
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//header//h1[@id="h1"]/text()').extract()[0]
        pubtime = response.xpath('//article/div[@class="gggs"]/time/text()').extract()[0]
        r = re.compile(u"(\d+)年(\d+)月(\d+)日(\d+):(\d+)")
        r = re.findall(r, pubtime)
        if not r:
            r = re.compile(u"(\d+)年(\d+)月(\d+)日")
            r = re.findall(r, pubtime)
        if not r:
            raise Exception(u"解析时间失败")
        r = [ int(x) for x in r[0] ]
        if len(r) == 3:
            pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2])
        else:
            pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4])
        htmlcontent = response.xpath('//div[contains(@class, "articulum")]').extract()[0]

        soup = BeautifulSoup(htmlcontent, "lxml")
        [d.extract() for d in soup.find_all("div", id="InRead")]
        [d.extract() for d in soup.find_all("div", id="goldenhorse")]
        [d.extract() for d in soup.find_all("div", id="teadstv")]
        [d.extract() for d in soup.find_all("div", id="textlink")]
        content = unicode(soup.body.contents[0])
        soup = BeautifulSoup(response.body, "lxml")
        figure = soup.select('article#maincontent div#rt_headpic > header + figure')
        video = soup.select('div#playerVideo')
        if figure:
            htmlcontent = u"<div>" + unicode(figure[0]) + content + "</div>"
        elif video:
            text = unicode(video[0])
            r = re.compile(u"url: '(.*?\.mp4)'")
            r = re.findall(r, text)
            if not r:
                raise Exception(u"解析mp4视频失败")
            src = r[0]
            htmlcontent = u"<div><div><video src=\"{}\"></video></div>".format(src) + content + "</div>"
        else:
            htmlcontent = content

        keywords = []
        source = u"蘋果日報"
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class AppledailyListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "appledaily_list"
    allowed_domains = ["appledaily.com.tw"]
    start_urls = (
        "http://www.appledaily.com.tw/realtimenews/section/new/",              # 最新
        "http://www.appledaily.com.tw/realtimenews/section/new/2",
        "http://www.appledaily.com.tw/realtimenews/section/new/3",
    )

    def parse(self, response):
        hrefs = response.xpath('//div[contains(@class, "abdominis")]/ul/li[contains(@class, "rtddt")]/a/@href').extract()
        appledaily = AppledailySpider()
        for _href in hrefs:
            href = "http://www.appledaily.com.tw" + _href
            if not Database.find_dup(href):
                yield scrapy.Request(href, callback=appledaily.parse)
