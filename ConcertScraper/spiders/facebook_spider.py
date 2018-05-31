import scrapy
import logging
import sys
from ConcertScraper.service.SlackNotification import SlackNotification

# fix ascii encode error on python2.7
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

log = logging.getLogger(__name__)


class FacebookSpider(scrapy.Spider):
    name = "facebook"
    custom_settings = {"DOWNLOADER_MIDDLEWARES": {'ConcertScraper.middlewares.FacebookDownloaderMiddleware': 543}}

    def start_requests(self):
        if self.settings["ENABLE_NOTI_SLACK"]:
            response = SlackNotification.sendMsg(self.settings["SLACK_WEBHOOK_URL"], "Start facebook spider.")
            if response != 200:
                log.error("Cannot send notfication slack when open spider")
        start_urls = self.settings["FACEBOOK_GROUP_SEARCH_URL"]
        keyword = self.settings["MAIN_SEARCH_KEYWORD"]
        for url in start_urls:
            url = url.format(keyword)
            log.info("Send request for facebook group URL = {}".format(url))
            yield scrapy.Request(url=url, callback=self.parse, meta={"facebook": True})

    def parse(self, response):
        if response.meta.get("facebook"):
            post_list = response.xpath("//div[@class='_307z']")
            for post in post_list:
                post_owner = post.xpath(".//div[@class='_vwp']//text()").extract_first()
                text_list = post.xpath(".//div[@class='_4rmu']//text()").extract()
                link = post.xpath(".//div[@class='_4rmu']//a//@href").extract_first()
                id = link[link.find("permalink") + 10:]
                id = id[:id.find("/")]
                yield {
                    "source": "facebook",
                    "id": id,
                    "title": post_owner,
                    "detail": ' '.join(text_list),
                    "price": None,
                    "contact": None,
                    "link": 'https://www.facebook.com' + link
                }

    # def parse(self, response):
    #     # We want to inspect one specific response.
    #     from scrapy.shell import inspect_response
    #     inspect_response(response, self)
    #
    #     # Rest of parsing code.
