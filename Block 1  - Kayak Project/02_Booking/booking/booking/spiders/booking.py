import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlencode, urlparse, parse_qsl
import sys
import os
import json
from datetime import datetime, timedelta
sys.path.append(os.path.abspath("C:\\Users\\Utilisateur\\Documents\\JEDHA\\03_Data_Collection_and_Management\\04_Kayak_Project\\02_Booking\\booking\\booking"))
from items import BookingItem
sys.path.append(os.path.abspath('C:/Users/Utilisateur/Documents/JEDHA/03_Data_Collection_and_Management/04_Kayak_Project/01_Weather'))
from weather import * # type: ignore


class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['booking.com']   
    start_urls = []

    def start_requests(self):
        #We open the data from the weather API to get the top 5 cities to scrap       
        df_weather,df_aggregated= read_weather_data() # type: ignore
        cities = df_aggregated[:5]['city'].unique()

        #We set a list of days for the next 7 days
        today= datetime.now()
        list_date = [((today+timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(1,8)]


        #For each city and each day, we search for the hotel and scrap the search page in parse_hotel
        for city in cities: 
            for i in range(len(list_date)-1):
                params={
                    'ss': city,
                    'checkin':list_date[i],
                    'checkout' : list_date[i+1],
                'group_adults':'2',
                'no_rooms':'1',
                'group_children':'0'
                    }
                url = 'https://www.booking.com/searchresults.fr.html?'
                url = url + urlencode(params)

                request = scrapy.Request(url, callback=self.parse_hotel)
                request.meta['city'] = city
                request.meta['checkin'] = list_date[i]
                request.meta['checkout'] = list_date[i+1]
                
                yield request
    
    #Here we take the 20 first hotel and get the main data. Then we open the hotel page. THe meta function is used to pass the information to the next request
    def parse_hotel(self,response):
        for hotel in response.css('div.c655c9a144')[0:20]:
            item = BookingItem()
            item['city'] = response.meta['city']
            item['name'] = hotel.css('div.e037993315.f5f8fe25fa::text').get()
            item['rank'] = hotel.css('div.d0522b0cca.fd44f541d8::text').get()
            item['number_ranking'] = hotel.css('div.e8acaa0d22.ab107395cb.c60bada9e4::text').get().split(' ')[0]
            item['checkin'] = response.meta['checkin']
            item['checkout'] = response.meta['checkout']
            item['price'] = hotel.css('span.e037993315.ab91cb3011.d9315e4fb0::text').get().replace("€ ","")
            item['distance'] = hotel.xpath('//span[@data-testid="distance"]/text()').get()

            secondary_page_url = response.urljoin(hotel.css('a.f0ebe87f68').attrib['href'])

            if secondary_page_url:
                    request = response.follow(secondary_page_url, self.parse_secondary_page)
                    request.meta['item'] = item
                    yield request

    #Here we get the missing data
    def parse_secondary_page(self,response):
        item = response.meta['item']
        item['adress'] = response.css('span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip::text').get().replace( '\n','')
        item['lat'] = response.css('a.loc_block_link_underline_fix.bui-link.show_on_map_hp_link.show_map_hp_link').attrib['data-atlas-latlng'].split(',')[0]
        item['lon'] =  response.css('a.loc_block_link_underline_fix.bui-link.show_on_map_hp_link.show_map_hp_link').attrib['data-atlas-latlng'].split(',')[1]
        item['description'] = response.css('p.e2585683de.c8d1788c8c::text').get()
        item['url'] = response.url
        yield item 

