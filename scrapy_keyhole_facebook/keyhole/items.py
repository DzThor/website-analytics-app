# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class KeyholeFacebookItem(scrapy.Item):
    source = scrapy.Field()
    platform = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    pageLikes = scrapy.Field()
    averageLikesFacebook = scrapy.Field()
    averageComments = scrapy.Field()
    averageShares = scrapy.Field()
    averageEngagement = scrapy.Field()
