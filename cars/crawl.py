#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from spiders.base_spider import BaseSpider


def main():
    # Load local settings
    settings = get_project_settings()

    # Run crawler
    process = CrawlerProcess(settings)
    process.crawl(BaseSpider)
    process.start()


if __name__ == '__main__':
    main()