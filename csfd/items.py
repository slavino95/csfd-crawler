# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CsfdItem(scrapy.Item):
    # define the fields for your item here like:

    movie = scrapy.Field()
    genre = scrapy.Field()
    origin = scrapy.Field()
    year = scrapy.Field()
    length = scrapy.Field()
    rating = scrapy.Field()
    director = scrapy.Field()
