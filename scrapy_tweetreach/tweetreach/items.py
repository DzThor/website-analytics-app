# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TweetreachItem(scrapy.Item):
   source = scrapy.Field()
   name = scrapy.Field()
   platform =scrapy.Field()
   date = scrapy.Field()
   accountsReached = scrapy.Field()
   impressions = scrapy.Field()
   top_contributors = scrapy.Field()
