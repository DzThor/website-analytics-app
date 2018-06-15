# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KeyholeItem(scrapy.Item):
    name = scrapy.Field()
    posts = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    avgRetweets = scrapy.Field()
    avgLikes = scrapy.Field()
    engRate = scrapy.Field()
    bio = scrapy.Field()
    website = scrapy.Field()
