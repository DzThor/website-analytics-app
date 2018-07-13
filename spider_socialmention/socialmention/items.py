# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SocialmentionItem(scrapy.Item):

    name = scrapy.Field()
    strengh = scrapy.Field()
    sentimentRatio = scrapy.Field()
    passion = scrapy.Field()
    reach = scrapy.Field()
    timePerMention = scrapy.Field()
    lastMention  = scrapy.Field()
    uniqueAuthors = scrapy.Field()
    retweets = scrapy.Field()
    sentimentList = scrapy.Field()
    keywordsList = scrapy.Field()
    usersList = scrapy.Field()
    hashtagsList = scrapy.Field()

