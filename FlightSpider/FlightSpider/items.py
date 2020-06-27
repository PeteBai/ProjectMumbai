# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlightspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    qry_dt = scrapy.Field()
    line = scrapy.Field()
    dep_tm = scrapy.Field()
    dep_ap = scrapy.Field()
    arr_tm = scrapy.Field()
    arr_ap = scrapy.Field()
    plane_type = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()


