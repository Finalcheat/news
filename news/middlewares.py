# -*- coding: utf-8 -*-

from private_settings import PROXY_CONFIG


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if getattr(spider, 'USE_PROXY', None) == True:
            request.meta['proxy'] = PROXY_CONFIG["http"]
