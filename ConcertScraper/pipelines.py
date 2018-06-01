# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
from ConcertScraper.service.Notification import Notification
import json
from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Bangkok')
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
        self.ENABLE_LINE_NOTI = spider.settings["ENABLE_LINE_NOTI"]
        self.CHANEL_ACCESS_TOKEN = spider.settings["CHANEL_ACCESS_TOKEN"]
        self.LINE_USER_ID_LIST = spider.settings["LINE_USER_ID_LIST"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_in_db = self.db[self.collection_name].find_one({"source": item["source"], "id": item["id"]})
        if item_in_db is None:
            # Send slack notification
            item_t = dict(item)
            item_t["created_date"] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            if self.ENABLE_NOTI_SLACK:
                slack_response = Notification.sendSlackMsg(self.SLACK_WEBHOOK_URL,
                                                           Notification.createMsgFromResult(item_t))
            if self.ENABLE_LINE_NOTI:
                line_response = Notification.sendLineMsg(self.CHANEL_ACCESS_TOKEN, self.LINE_USER_ID_LIST
                                                         , Notification.createMsgFromResult(item_t))
            if (self.ENABLE_NOTI_SLACK and slack_response.status_code == 200) or (
                    self.ENABLE_LINE_NOTI and line_response.status_code == 200):
                log.info("Not found cache item, insert one src = {}, id = {}".format(item_t["source"], item_t["id"]))
                self.db[self.collection_name].insert_one(item_t)
            else:
                if self.ENABLE_NOTI_SLACK and slack_response.status_code != 200:
                    log.error("Cannot send slack notification res code = {}, not item id = {}".format(
                        slack_response.status_code, item_t["id"]))
                if self.ENABLE_LINE_NOTI and line_response.status_code != 200:
                    log.error("Cannot send line notification res code = {}, not item id = {}".format(
                        line_response.status_code, item_t["id"]))
        else:
            log.info("Found cache item, drop item src = {}, id = {}".format(item["source"], item["id"]))
        return item
