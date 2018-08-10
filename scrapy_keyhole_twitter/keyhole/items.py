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
    followers = scrapy.Field()
    following = scrapy.Field()
    avgRetweets = scrapy.Field()
    avgLikes = scrapy.Field()
    engRate = scrapy.Field()
    bio = scrapy.Field()
    website = scrapy.Field()

class KeyholeFacebookItem(scrapy.Item):
    source = scrapy.Field()
    platform = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    pageLikes = scrapy.Field()
    avgLikes = scrapy.Field()
    avgComments = scrapy.Field()
    avgShares = scrapy.Field()
    avgEngRate = scrapy.Field()
