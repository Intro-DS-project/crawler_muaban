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
    
    def to_dict(self):
        return {
            'price': self.get('price'),
            'area': self.get('area'),
            'num_bedroom': self.get('num_bedroom'),
            'num_diningroom': self.get('num_diningroom'),
            'num_kitchen': self.get('num_kitchen'),
            'num_toilet': self.get('num_toilet'),
            'num_floor': self.get('num_floor'),
            'current_floor': self.get('current_floor'),
            'street': self.get('street'),
            'ward': self.get('ward'),
            'district': self.get('district'),
            'direction': self.get('direction'),
            'street_width': self.get('street_width'),
            'post_date': self.get('post_date'),
            'description': self.get('description'),
            'url': self.get('url')
        }
