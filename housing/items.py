# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class HousingItem(Item):
    _id = Field()
    title = Field()
    price = Field()
    rooms = Field()
    area = Field()
    baths = Field()
    address = Field()
    lat = Field()
    lon = Field()
