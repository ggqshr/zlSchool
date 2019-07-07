# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import redis as r
from pymongo import MongoClient
from .settings import MODE
from .settings import REDIS_HOST, REDIS_PORT, MONGODB_HOST, MONGODB_PORT

LOCAL = "127.0.0.1"


class ZlschoolPipeline(object):
    def __init__(self):
        self.client = r.Redis(REDIS_HOST if MODE == 'LOCAL' else LOCAL, port=REDIS_PORT)
        self.conn = MongoClient(MONGODB_HOST if MODE == 'LOCAL' else LOCAL, MONGODB_PORT)
        self.mongo = self.conn.ZLSchool.ZLSchool
        self.count = 0

    def process_item(self, item, spider):
        self.count += 1
        if self.client.sadd("ZL_set", item['id']) == 0:
            return item
        self.mongo.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        with open("result.log", "a") as f:
            f.writelines("{} crawl item {} \n".format(datetime.now().strftime("%Y.%m.%d"), self.count))
            f.flush()
