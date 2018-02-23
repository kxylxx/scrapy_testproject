# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import re
from scrapy import Spider, Request

from scrapy_mmwz.items import mmwzItem


class XinwenSpider(Spider):
    name = "xinwen"
    keyword = '比特币'
    page = 0
    data = {
        'word': keyword,
        'pn': page,
        'cl': '2',
        'ct': '1',
        'tn': 'news',
        'rn': '20',
        'ie': 'utf - 8',
        'bt': '0',
        'et': ' 0'
    }
    # 生成URL的参数部分
    params = urlencode(data)
    base = 'http://news.baidu.com/ns?'
    url = base + params
    allowed_domains = ["news.baidu.com"]
    start_urls = [url]

    def parse(self, response):
        item = mmwzItem()
        if response.status == 200:
            # print(response.text)
            # 用pyquery来解析网页
            news_lists = response.css('#wrapper_wrapper #content_left div.result')
            page_number = response.css('p#page strong span.pc::text').extract()
            # print(news_lists)
            print('11111111111111111')
            print('page_number:', page_number)
            if news_lists:
                for news in news_lists:
                    # 这是一个生成器，在调用函数是可以用for循环依次获取结果，它相当于return只不过一次返回一个
                    lists = {
                        'article_url': news.css('.c-title a::attr(href)').extract_first(),
                        'article_title': news.css('.c-title a::text').extract_first(),
                        'article_catchroad': 'baidu',
                        'article_source': re.search(re.compile('(.*?)\\xa0', re.S),
                                                    news.css('p.c-author::text').extract_first()).group(1)
                    }
                    for field in item.fields:
                        if field in lists.keys():
                            item[field] = lists.get(field)
                    yield item
            print(response.css('p#page a:last-child::text').extract_first())
            if response.css('p#page a:last-child::text').extract_first() == '下一页>':
                next_page = 'http://news.baidu.com' + response.css('p#page a:last-child::attr(href)').extract_first()
                yield Request(next_page, callback=self.parse)



