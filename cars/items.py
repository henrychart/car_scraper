# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field
import scrapy

class Cars(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    Engine_Litre = Field()
    Mileage = Field()
    BHP = Field()
    Fuel = Field()
    Manual = Field()
    Price = Field()
    Desc = Field()
    Title = Field()
