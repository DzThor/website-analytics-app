# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FollerItem(scrapy.Item):
    username = scrapy.Field()
    tweets = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    followers_ratio = scrapy.Field()
    topics = scrapy.Field()
    hashtags = scrapy.Field()
    replies_100 = scrapy.Field()
    mentions_100 = scrapy.Field()
    hashtags_100 = scrapy.Field()
    retweets_100 = scrapy.Field()
    links_100 = scrapy.Field()
    media_100 = scrapy.Field()
    linked_domains_100 = scrapy.Field()
    twitter_clients_100 = scrapy.Field()