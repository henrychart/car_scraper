from base_spider import BaseSpider
import scrapy
from cars.items import Cars
from scrapy.loader import ItemLoader

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
        # l = ItemLoader(item=Cars(), response=response)
        # l.add_xpath('Price', '//span[@class="item--price"]/text()')
        # l.add_xpath('Title', '//h1[@class="main--title grid__item three-quarters"]/text()')
        # l.add_xpath('Desc', '//section[@class="advert-description"]/text()')

        price = response.xpath('//span[@class="item--price"]/text()').extract()
        title = response.xpath('//h1[@class="main--title grid__item three-quarters"]/text()').extract()
        desc = response.xpath('//section[@class="advert-description"]/text()').extract()

        result = dict(zip([f.extract() for f in response.xpath("//ul[@class ='specs-list']//span[@class ='specs-list__item__name']/text()")],
            [[f.extract()] for f in response.xpath("//ul[@class='specs-list']//span[@class='specs-list__item__value']/text()")]))

        result['Price'] = price
        result['Title'] = ['^&'.join(title)]
        result['Desc'] = ['^&'.join(desc)]

        yield result


        # print l.load_item()


    # def extract_results(self, response):
    #     price = response.xpath('//span[@class="item--price"]/text()').extract_first()
    #     features = response.xpath('//ul[@class="feature-specs"]')
    #     desc = response.xpath('//section[@class="advert-description"]/text()').extract_first()
    #     title = response.xpath('//h1[@class="main--title grid__item three-quarters"]/text()').extract_first()
    #     yield dict(zip(['Engine_Litre','Mileage','BHP','Fuel','Manual','Price', 'Desc', 'Title'], [f.extract() for f in features.xpath('.//p/text()')] + [price] + [desc] + [title]))


#l.add_xpath(a, b) for a, b in zip(['Engine_Litre', 'Mileage', 'BHP', 'Fuel', 'Manual'], [f.extract() for f in features.xpath('.//p/text()')])]