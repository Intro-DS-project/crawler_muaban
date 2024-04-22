from typing import Iterable
import scrapy 
from crawler_muaban.items import MuabanItem
from crawler_muaban.api import extract_description
from datetime import date, timedelta
#import sleep 
import time

# thoi gian hom nay
today =  date.today().strftime("%d/%m/%Y")


class MuabanSpider(scrapy.Spider):
      name = 'muaban'
      allowed_domains = ['muaban.net']
      start_urls = ['https://muaban.net/']
      def start_requests(self):
            pages = []
            for i in range(1, 10):
                  domain = 'https://muaban.net/bat-dong-san/cho-thue-nha-tro-phong-tro-ha-noi#page={}'.format(i)
                  pages.append(domain)
            for page in pages:
                  yield scrapy.Request(url=page, callback=self.parse_link)

      
      def parse_link(self, response):
            for i in range(1, 10):
                  str = "#__next > div.sc-11qpg5t-0.sc-1b0gpch-0.dDFAEo.YcQzv > div.sc-1b0gpch-1.dXYEMQ > div.sc-1b0gpch-2.hRxuIG > div > div > div:nth-child({}) > div > div.sc-q9qagu-14.eOzaio > div > a::attr(href)".format(i)
                  link = response.css(str).extract_first()                  
                  link = "https://muaban.net" + link          
                  yield scrapy.Request(url=link, callback=self.parse)
      def parse(self, response, **kwargs):
            item = MuabanItem()
            item['price'] = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/text()').extract_first()
            address = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[2]/text()').extract_first()
            if address is not None:
                  address = address.split(', ')
                  if len(address):
                        item['street'] = address[-4]
                        item['ward'] = address[-3]
                        item['district'] = address[-2]
            date = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[3]/text()')[1].get()
            
            item['post_date'] = date_convert(date)
            item['description'] = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[4]/div/text()').extract_first()
            item['area'] = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[6]/div[1]/ul/li/span[2]/text()').extract_first()
            item['url'] = response.request.url

            fields = extract_description(" ".join(item['description'])).split(',')
            fields_int = []
            for field in fields:
                    try:
                              fields_int.append(int(field))
                    except ValueError:
                              fields_int.append(field)
            item["num_bedroom"], item["num_diningroom"], item["num_kitchen"], item["num_toilet"], item["num_floor"], \
            item["current_floor"], item["direction"], item["street_width"], *_ = fields_int

            yield item

def date_convert(date):
       if date is not None:
             if date == "Hôm nay":
                   return today
             elif date == "Hôm qua":
                   return (date.today() - timedelta(1)).strftime("%d/%m/%Y")
             else:
                   return date


      