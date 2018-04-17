from base_spider import BaseSpider
import scrapy

class SearchCarSpider(BaseSpider):

    relative_url = 'https://www.pistonheads.com/'
    name = 'search_car_spider'

    def parse_search_results(self, response):
        self.crawler.stats.inc_value('car/search/request')
        # Extract urls
        links = response.xpath('//div[@class="listing-headline"]/a[@href]/@href').extract()
        for link in links:
            yield scrapy.Request(url=self.base_url + link, callback=self.extract_results, errback=self.process_search_error)

        relative_next_url = response.xpath('//li[@class=" next"]/a[@href]/@href').extract_first()
        absolute_next_url = '{}{}'.format(self.base_url, relative_next_url)
        if absolute_next_url:
            yield scrapy.Request(absolute_next_url, callback=self.parse_search_results)

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
        desc = response.xpath('//section[@class="advert-description"]/text()').extract_first()
        title = response.xpath('//h1[@class="main--title grid__item three-quarters"]/text()').extract_first()
        yield dict(zip(['Engine_Litre','Mileage','BHP','Fuel','Manual','Price', 'Desc', 'Title'], [f.extract() for f in features.xpath('.//p/text()')] + [price] + [desc] + [title]))
