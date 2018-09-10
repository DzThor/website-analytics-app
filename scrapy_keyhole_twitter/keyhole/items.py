# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KeyholeTwitterItem(scrapy.Item):
    source = scrapy.Field()
    platform = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    tweets = scrapy.Field()
    #followers = scrapy.Field()
    following = scrapy.Field()
    averageRetweets = scrapy.Field()
    averageLikesTwiiter = scrapy.Field()
    averageEngRate = scrapy.Field()
    bio = scrapy.Field()
    website = scrapy.Field()
