# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
from ConcertScraper.service.SlackNotification import SlackNotification
import json
import datetime

log = logging.getLogger(__name__)


class MongoDBPipeline(object):
    collection_name = 'result_cache'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.SLACK_WEBHOOK_URL = spider.settings["SLACK_WEBHOOK_URL"]
        self.ENABLE_NOTI_SLACK = spider.settings["ENABLE_NOTI_SLACK"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_in_db = self.db[self.collection_name].find_one({"source": item["source"], "id": item["id"]})
        if item_in_db is None:
            # Send slack notification
            if self.ENABLE_NOTI_SLACK:
                item = dict(item)
                item["created_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                response = SlackNotification.sendMsg(self.SLACK_WEBHOOK_URL, json.dumps(item))
                if response.status_code == 200:
                    log.info("Not found cache item, insert one src = {}, id = {}".format(item["source"], item["id"]))
                    self.db[self.collection_name].insert_one(item)
                else:
                    log.error("Cannot send slack notification response code {}".format(response.status_code))
        else:
            log.info("Found cache item, drop item src = {}, id = {}".format(item["source"], item["id"]))
        return item
