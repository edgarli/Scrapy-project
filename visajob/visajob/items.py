# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VisajobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company = scrapy.Field()
    Total_visa = scrapy.Field()
    salary = scrapy.Field()
    certified = scrapy.Field()
    c_withdraw = scrapy.Field()
    denied = scrapy.Field()
    withdraw = scrapy.Field()
    job_location = scrapy.Field()
    job_name = scrapy.Field()
    year = scrapy.Field()
    number_j_location = scrapy.Field()
    number_j_name = scrapy.Field()
