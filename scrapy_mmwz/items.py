# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class mmwzItem(Item):
    # define the fields for your item here like:
    # name = Field()
    article_title = Field()
    article_url = Field()
    article_catchroad = Field()
    article_source = Field()
