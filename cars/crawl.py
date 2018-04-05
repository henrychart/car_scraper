#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from spiders.main_generate_links import SearchCarSpider


def main():
    # Load local settings
    settings = get_project_settings()

    # Run crawler
    process = CrawlerProcess(settings)
    process.crawl(SearchCarSpider)
    process.start()


if __name__ == '__main__':
    main()