# -*- coding: utf-8 -*-
from pymongo import MongoClient
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AiwancrawlPipeline(object):
    collection = None

    def open_spider(self, spider):
        db2 = MongoClient(host='192.168.19.29').get_database(name='db2')
        self.collection = db2.get_collection('mycrawl')
        # print(self.collection)

    def process_item(self, item, spider):
        title = item['title']
        play_times = item['play_times']
        role = item['role']
        director = item['director']
        introduction = item['introduction']
        dic = {
            'title': title,
            'play_times': play_times,
            'role': role,
            'director': director,
            'introduction': introduction,
        }
        self.collection.insert(dic)
        return item


