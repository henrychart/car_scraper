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
        price = response.xpath('//span[@class="item--price"]/text()').extract()
        engine_litre = response.xpath('//ul[@class="feature-specs"]//p[@xpath = "1"]/text()')#.extract()
        mileage = response.xpath('//ul[@class="feature-specs"]//p[@xpath="2"]/text()').extract()
        bhp = response.xpath('//ul[@class="feature-specs"]//p[@xpath="3"]/text()').extract()
        fuel = response.xpath('//ul[@class="feature-specs"]//p[@xpath="4"]/text()').extract()
        gearbox = response.xpath('//ul[@class="feature-specs"]//p[@xpath="5"]/text()').extract()
        print price
        print engine_litre
        print mileage
        print bhp
        print fuel
        print gearbox

    # Vechile description


