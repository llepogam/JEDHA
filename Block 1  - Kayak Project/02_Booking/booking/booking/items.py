# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class BookingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    rank = scrapy.Field()
    number_ranking = scrapy.Field()
    price = scrapy.Field()
    checkin = scrapy.Field()
    checkout = scrapy.Field()
    adress = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    distance = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()

    
