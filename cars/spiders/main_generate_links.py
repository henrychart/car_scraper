from base_spider import BaseSpider
import scrapy

class SearchCarSpider(BaseSpider):

    name = 'search_car_spider'

    def parse_search_results(self, response):
        self.crawler.stats.inc_value('car/search/request')
        # Extract urls
        links = response.xpath('//div[@class="listing-headline"]/a[@href]/@href').extract()
        for link in links:
            #yield #self.base_url + link #(workout how to yeild the results)
            yield scrapy.Request(url=self.base_url + link, callback=self.extract_results, errback=self.process_search_error)

    def process_search_error(self, failure):
        self.crawler.stats.inc_value('car/search/request')
        yield {
            'result_type': 'web_search_result',
            'request_url': failure.value.response.url,
            'result_url': None
        }


    def extract_results(self, response):
        price = response.xpath('//span[@class="item--price"]/text()').extract_first()
        features = response.xpath('//ul[@class="feature-specs"]')
        print dict(zip(['Engine_Litre','Mileage','BHP','Fuel','Manual','Price'], [f.extract() for f in features.xpath('.//p/text()')] + [price]))



    # Vechile description
    # Vechile title
    # Handiling next page


