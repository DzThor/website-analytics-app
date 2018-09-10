# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FollerItem(scrapy.Item):
    source = scrapy.Field()
    platform = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    tweets = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    followers_ratio = scrapy.Field()
    topics = scrapy.Field()
    hashtags = scrapy.Field()
    xtweets = scrapy.Field()
    replies_for_xtweets = scrapy.Field()
    mentions_for_xtweets = scrapy.Field()
    hashtags_for_xtweets = scrapy.Field()
    retweets_for_xtweets = scrapy.Field()
    links_for_xtweets = scrapy.Field()
    media_for_xtweets = scrapy.Field()
    linked_domains_for_xtweets = scrapy.Field()
    twitter_clients_for_xtweets = scrapy.Field()
    tweetingSchedule = scrapy.Field()