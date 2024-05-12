from typing import Iterable
import scrapy 
from crawler_muaban.items import MuabanItem
from crawler_muaban.api import extract_description
from datetime import date, timedelta
from hanoikovoidcdau import standardize 
#import sleep 
from crawler_muaban.remote_database import init
import time

# thoi gian hom nay
today =  date.today().strftime("%d/%m/%Y")


class MuabanSpider(scrapy.Spider):
      name = 'muaban'
      allowed_domains = ['muaban.net']
      start_urls = ['https://muaban.net/']
      supabase = init()
      def start_requests(self):
            pages = []
            for i in range(1, 5):
                  domain = 'https://muaban.net/bat-dong-san/cho-thue-nha-tro-phong-tro-ha-noi?page={}'.format(i)
                  pages.append(domain)
            for page in pages:
                  yield scrapy.Request(url=page, callback=self.parse_link)

      
      def parse_link(self, response):
            for i in range(1, 21):
                  str = "#__next > div.sc-11qpg5t-0.sc-1b0gpch-0.dDFAEo.YcQzv > div.sc-1b0gpch-1.dXYEMQ > div.sc-1b0gpch-2.hRxuIG > div > div.sc-q9qagu-3.jcgEeF > div:nth-child({}) > div > div.sc-q9qagu-13.cSoxyz > div > a::attr(href)".format(i)
                  link = response.css(str).extract_first()          
                  link = "https://muaban.net" + link     
                  if link is not None:
                        q_area= "#__next > div.sc-11qpg5t-0.sc-1b0gpch-0.dDFAEo.YcQzv > div.sc-1b0gpch-1.dXYEMQ > div.sc-1b0gpch-2.hRxuIG > div > div.sc-q9qagu-3.jcgEeF > div:nth-child({}) > div > div.sc-q9qagu-13.cSoxyz > div > ul > li::text".format(i)
                        area = response.css(q_area).extract_first()
                        q_price = "#__next > div.sc-11qpg5t-0.sc-1b0gpch-0.dDFAEo.YcQzv > div.sc-1b0gpch-1.dXYEMQ > div.sc-1b0gpch-2.hRxuIG > div > div.sc-q9qagu-3.jcgEeF > div:nth-child({}) > div > div.sc-q9qagu-13.cSoxyz > div > span::text".format(i)
                        q_date = "#__next > div.sc-11qpg5t-0.sc-1b0gpch-0.dDFAEo.YcQzv > div.sc-1b0gpch-1.dXYEMQ > div.sc-1b0gpch-2.hRxuIG > div > div.sc-q9qagu-3.jcgEeF > div:nth-child({}) > div > div.sc-q9qagu-13.cSoxyz > ul > li.sc-q9qagu-10.sc-q9qagu-11.eHidYL.gVECmZ > span:nth-child(2)::text".format(i) 
                        price = response.css(q_price).extract_first()
                        date = response.css(q_date).extract_first()
                        area = format_area(area)
                        price = format_price(price)
                        date = format_date(date)
                  # nếu post_dâte là hôm nay hoặc hôm qua thì mới lấy thông tin
                  if date == today:
                          yield response.follow(link, self.parse, meta={'area': area, 'price': price, 'post_date': date})

                  



                  # yield response.follow(link, self.parse, meta={'area': area, 'price': price, 'post_date': date})
      def parse(self, response, **kwargs):
            item = MuabanItem()
            item['area'] = response.meta['area']
            item['price'] = response.meta['price']
            item['post_date'] = response.meta['post_date']
            # nếu post_dâte là hôm nay hoặc hôm qua thì mới lấy thông tin 
            

            expired = response.css("#__next > div.sc-ed7dq4-0.dMIoxZ > div.sc-11qpg5t-0.sc-ed7dq4-4.dDFAEo.jiSzNj > span > p:nth-child(2)").extract_first()
            #__next > div.sc-ed7dq4-0.dMIoxZ > div.sc-11qpg5t-0.sc-ed7dq4-4.dDFAEo.jiSzNj > span > p:nth-child(2)
            if expired is None:
                  # price = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/text()').extract_first()
                  # item['price'] = format_price(price)

                  address = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[2]/text()').extract_first()

                  if address is not None:
                        address = address.split(', ')
                        if len(address):
                              item['street'] = address[-4]
                              item['ward'] = address[-3]
                              item['district'] = address[-2]
                              item["street"] = standardize.standardize_street_name(item["street"])
                              item["ward"] = standardize.standardize_ward_name(item["ward"])
                              item["district"] = standardize.standardize_district_name(item["district"])
                  # date = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[3]/text()')[1].get()                  
                  # item['post_date'] = date_convert(date)
                  item['description'] = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[4]/div/text()').extract_first()
                  area = response.xpath('//*[@id="__next"]/div[2]/div[3]/div/div[1]/div[2]/div[6]/div[1]/ul/li/span[2]/text()').extract_first()
                  # item['area'] = format_area(area)
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
                  # data, count = self.supabase.table("entries").insert([item.to_dict()]).execute()
            
            else: 
                  # price = response.xpath('//*[@id="__next"]/div[2]/div[5]/div/div[1]/div[2]/div[2]/div[1]/div/text()').extract_first()
                  # item['price'] = format_price(price)

                  address = response.xpath('//*[@id="__next"]/div[2]/div[5]/div/div[1]/div[2]/div[2]/div[2]/text()').extract_first()

                  if address is not None:
                        address = address.split(', ')
                        if len(address):
                              item['street'] = address[-4]
                              item['ward'] = address[-3]
                              item['district'] = address[-2]
                              item["street"] = standardize.standardize_street_name(item["street"])
                              item["ward"] = standardize.standardize_ward_name(item["ward"])
                              item["district"] = standardize.standardize_district_name(item["district"])
                  # date = response.xpath('//*[@id="__next"]/div[2]/div[5]/div/div[1]/div[2]/div[2]/div[3]/text()')[1].get()                  
                  # item['post_date'] = date_convert(date)
                  item['description'] = response.xpath('//*[@id="__next"]/div[2]/div[5]/div/div[1]/div[2]/div[4]/div[1]/text()').extract_first()
                  # area = response.xpath('//*[@id="__next"]/div[2]/div[5]/div/div[1]/div[2]/div[6]/div[1]/ul/li[2]/span[2]/text()').extract_first()
                  # .                    //*[@id="__next"]/div[2]/div[5]/div/div[1]/div[2]/div[6]/div[1]/ul/li/span[2]
                  # item['area'] = format_area(area)
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
                   



def format_date(date):
       if date is not None:
             if date == "Hôm nay":
                   return today
             elif date == "Hôm qua":
                   return (date.today() - timedelta(1)).strftime("%d/%m/%Y")
             else:
                   return date
def format_price(price):
       # convert miliion to int
       price = price.split(' ')[0]
       price = float(price.replace('.', ''))/10**6
       return price

def format_area(area):
       # convert m2 to int
       return float(area.split(' ')[0])
      