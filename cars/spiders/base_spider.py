# -*- coding: utf-8 -*-

import scrapy


class BaseSpider(scrapy.Spider):

    base_url = 'https://www.pistonheads.com'
    name = 'base_spider'

    def process_car_name(self, car):
        return '{}/classifieds/used-cars/{}'.format(self.base_url, car)

    def load_requests(self):
        """
        Load car names from an input and create search urls
        :return:
        """
        cars = ['ferrari', 'bmw']
        #cars = self.settings.get('INPUT_DATA', [])
        return [self.process_car_name(car) for car in cars]

    def start_requests(self):

        for url in self.load_requests():
            self.crawler.stats.inc_value('car/search/request')
            yield scrapy.Request(url=url, callback=self.parse_search_results, errback=self.process_search_error)


    def parse_search_results(self, response):
        print response
        yield {'request_url': response.url}

    def process_search_error(self, failure):
        yield {'request_url': failure.value.response.url}

