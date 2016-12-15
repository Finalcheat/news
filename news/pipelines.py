# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from bs4 import BeautifulSoup
from scrapy.exceptions import DropItem


class NewsPipeline(object):
    def process_item(self, item, spider):
        return item


class NewsHtmlcontentPipeline(object):
    """
    删除html标签属性
    """

    def remove_html_comments(self, html):
        """
        删除掉html注释<!-- -->
        """
        r = re.compile("<!--.*?-->")
        return re.sub(r, "", html)

    def process_item(self, item, spider):
        # print spider
        htmlcontent = item["htmlcontent"]
        # print htmlcontent
        soup = BeautifulSoup(htmlcontent, "lxml")
        # 删除script标签
        [s.extract() for s in soup('script')]
        # 遍历子元素删除属性，只保留img的src和alt
        # 同时找出所有的img
        images = []
        for child in soup.descendants:
            try:
                attrs = child.attrs
                name = child.name
                if name == "iframe":
                    raise DropItem(u"存在iframe标签暂时未解析抛弃!")
                elif name == "img":
                    src, alt = attrs["src"], attrs.get("alt", "")
                    images.append({"src": src, "alt": alt})
                    child.attrs = {"src": src, "alt": alt}
                else:
                    child.attrs = {}
            except:
                pass
        new_htmlcontent = unicode(soup.body.contents[0])
        new_htmlcontent = self.remove_html_comments(new_htmlcontent)
        # print new_htmlcontent
        item["htmlcontent"] = new_htmlcontent
        item["images"] = images
        return item
