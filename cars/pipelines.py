# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pandas as pd
# import os
# import csv


class CarsPipeline(object):
    # Clean Search Results
    def process_item(self, item, spider):

        df = pd.DataFrame(item)
        df.to_csv('~/test_extract_cars.csv', header=None, index=False, mode='a', encoding='utf-8')
        print df.head()
        return item
