import scrapy
import logging
import sys
from ConcertScraper.service.Notification import Notification

# fix ascii encode error on python2.7
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

log = logging.getLogger(__name__)


class PantipMarketSpider(scrapy.Spider):
    name = "pantipmarket"
    start_url = 'https://www.pantipmarket.com/search/?keyword={}&group=11&show_adv=0'

    def start_requests(self):
        if self.settings["ENABLE_NOTI_SLACK"] and self.settings["ENABLE_SPIDER_START_NOTI"]:
            slack_response = Notification.sendLineMsg(self.settings["SLACK_WEBHOOK_URL"], "Start PantipMarket spider.")
            if slack_response.status_code != 200:
                log.error("Cannot send notification slack when open spider")
        if self.settings["ENABLE_LINE_NOTI"] and self.settings["ENABLE_SPIDER_START_NOTI"]:
            line_response = Notification.sendLineMsg(self.settings["CHANEL_ACCESS_TOKEN"], self.settings["LINE_USER_ID_LIST"]
                                                     , "Start PantipMarket spider.")
            if line_response.status_code != 200:
                log.error("Cannot send notification line when open spider")
        url = self.start_url.format(self.settings["MAIN_SEARCH_KEYWORD"])
        log.info("Send request for PantipMarket URL = {}".format(self.start_url))
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.xpath("//li[@class='ads_data']"):
            title = ''.join(item.xpath(".//div[@itemprop='name']//text()").extract())
            detail = ''.join(item.xpath(".//div[@class='listA_detail']//text()").extract())
            price = item.xpath(".//div[@class='listA_price']//span//text()").extract_first()
            contact = item.xpath(".//div[@class='listA_contact']//text()").extract()[2]
            contact = ' '.join(contact.split())
            id = item.xpath(".//i[@itemprop='productID']//@content").extract_first()
            link = "https://www.pantipmarket.com/items/" + id
            yield {
                "source": "pantipmarket",
                "id": id,
                "title": title,
                "detail": detail,
                "price": price,
                "contact": contact,
                "link": link
            }

    # def parse(self, response):
    #     # We want to inspect one specific response.
    #     from scrapy.shell import inspect_response
    #     inspect_response(response, self)
    #
    #     # Rest of parsing code.
