# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    pubtime = scrapy.Field()
    htmlcontent = scrapy.Field()
    keywords = scrapy.Field()
    source = scrapy.Field()
    href = scrapy.Field()
