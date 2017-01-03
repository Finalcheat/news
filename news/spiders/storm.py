# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from bs4 import BeautifulSoup
from news.items import NewsItem
from news.database import Database


class StormSpider(scrapy.Spider):
    USE_PROXY = True
    name = "storm"
    allowed_domains = ["storm.mg"]
    # start_urls = (
    #     "http://www.storm.mg/article/163066",
    # )

    def parse(self, response):
        href = response.url
        title = response.xpath('//h1[@id="article_title"]/text()').extract()[0]
        title = title.replace("\n", "").strip()
        pubtime = response.xpath('//div[@class="author_date"]/span[@class="date"]/text()').extract()[0]
        r = re.compile(u"(\d+)年(\d+)月(\d+)日 (\d+):(\d+)")
        r = re.findall(r, pubtime)
        if not r:
            raise Exception(u"解析时间失败")
        r = [ int(x) for x in r[0] ]
        pubtime = datetime.datetime(year=r[0], month=r[1], day=r[2], hour=r[3], minute=r[4])
        htmlcontent = response.xpath('//div[@class="content-main"]/div/div[@class="article-wrapper"]/article').extract()[0]

        soup = BeautifulSoup(htmlcontent, "lxml")
        [d.extract() for d in soup.select('div.ad_article_block')]
        [d.extract() for d in soup.select('div.like-box-wrapper_view')]
        [d.extract() for d in soup.select('div.like-box-wrapper')]
        [d.extract() for d in soup.select('div.like-box-wrapper_world')]
        [d.extract() for d in soup.select('div.like-box-wrapper_senior')]
        [d.extract() for d in soup.select('div.clear-float')]
        [u.extract() for u in soup.select('ul.manual-related')]
        [d.extract() for d in soup.select('div.keywords')]
        [d.extract() for d in soup.select('div#div-inread-ad')]
        [a.extract() for a in soup.select('a[rel="nofollow"]')]
        [d.extract() for d in soup.select('div.life_bottom')]
        [d.extract() for d in soup.select('div[id^="div-gpt-ad"]')]
        htmlcontent = unicode(soup.body.contents[0])

        keywords = []
        source = u"風傳媒"
        item = NewsItem(title=title, pubtime=pubtime, htmlcontent=htmlcontent, href=href, keywords=keywords, source=source)
        yield item


class StormListSpider(scrapy.Spider):
    USE_PROXY = True
    name = "storm_list"
    allowed_domains = ["storm.mg"]
    start_urls = (
        'http://www.storm.mg/category/2',             # 评论
        'http://www.storm.mg/category/118',           # 政治
        'http://www.storm.mg/category/117',           # 国际
        'http://www.storm.mg/category/22172',         # 国内
        'http://www.storm.mg/category/121',           # 中港澳
        'http://www.storm.mg/category/23083',         # 财经
        'http://www.storm.mg/category/24667',         # 调查
        'http://www.storm.mg/category/26644',         # 军事
        'http://www.storm.mg/lifestyles',             # 风生活
        'http://www.storm.mg/stylish-category',       # 品味生活
        'http://www.storm.mg/localarticles',          # 地方新闻
        'http://www.storm.mg/category/36291',         # 学长姐说
        'http://www.storm.mg/category/36948',         # 风数据
        'http://www.storm.mg/category/25421',         # 风摄影
        'http://www.storm.mg/category/22631',         # 好文推荐
        'http://www.storm.mg/category/965',           # 公民运动
        'http://www.storm.mg/category/22168',         # 公共政策
        'http://www.storm.mg/category/992',           # 观点投书
        'http://www.storm.mg/category/23440',         # 风书房
    )

    def parse(self, response):
        hrefs = response.xpath('//div[@class="main_content"]/a/@href').extract()
        storm = StormSpider()
        for _href in hrefs:
            if _href:
                href = "http://www.storm.mg" + _href
                if not Database.find_dup(href):
                    yield scrapy.Request(href, callback=storm.parse)
