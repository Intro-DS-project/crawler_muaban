# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MuabanItem(scrapy.Item):
    price = scrapy.Field()
    area = scrapy.Field()
    num_bedroom = scrapy.Field()
    num_diningroom = scrapy.Field()
    num_kitchen = scrapy.Field()
    num_toilet = scrapy.Field()
    num_floor = scrapy.Field()
    current_floor = scrapy.Field()
    street = scrapy.Field()
    ward = scrapy.Field()
    district = scrapy.Field()
    direction = scrapy.Field()
    street_width = scrapy.Field()
    post_date = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
