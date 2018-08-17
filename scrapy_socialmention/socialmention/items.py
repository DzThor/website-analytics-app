# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SocialmentionItem(scrapy.Item):

    source = scrapy.Field()

    name = scrapy.Field()
    platform = scrapy.Field()
    date = scrapy.Field()
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
    sentimentValues = scrapy.Field()
    keywordsValues = scrapy.Field()
    usersValues = scrapy.Field()
    hashtagsValues = scrapy.Field()

        #box grey text
        #//h4[contains(text(),"Sentiment")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]
        #//h4[contains(text(),"Top Keywords")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]
        #//h4[contains(text(),"Top Users")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]
        #//h4[contains(text(),"Top Hashtags")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]