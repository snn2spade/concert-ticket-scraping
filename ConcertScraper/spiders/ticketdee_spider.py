import scrapy
from ConcertScraper.service.TextUtility import TextUtility
import logging
import sys
from ConcertScraper.service.SlackNotification import SlackNotification

# fix ascii encode error on python2.7
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

log = logging.getLogger(__name__)


class TicketDeeSpider(scrapy.Spider):
    name = "ticketdee"
    url = 'https://www.ticketdee.com/apif/concert/search'
    url2 = 'https://www.ticketdee.com/apif/concert/{}/edit'

    def start_requests(self):
        if self.settings["ENABLE_NOTI_SLACK"]:
            response = SlackNotification.sendMsg(self.settings["SLACK_WEBHOOK_URL"], "Start TicketDee spider.")
            if response != 200:
                log.error("Cannot send notfication slack when open spider")
        self.keywords = self.settings["OTHER_SEARCH_KEYWORDS"]
        self.keywords.append(self.settings["MAIN_SEARCH_KEYWORD"])
        log.debug("SEARCH KEYWORDS = {}".format(self.keywords))
        log.info("Send request for TicketDee URL = {}".format(self.url))
        yield scrapy.FormRequest(url=self.url,
                                 formdata={'page': '1', 'show_sold_out': 'false', 'sortby': '2'},
                                 callback=self.parse)

    def parse(self, response):
        res = response.body.decode()
        res = res.replace('true', 'True')
        res = res.replace('false', 'False')
        res = res.replace('null', 'None')
        res = eval(res)
        currentPage = res[0]['currentPage']
        item_list = res[0]['v']
        for item in item_list:
            if TextUtility.find_in_text(item["title"], self.keywords) >= 0:
                request = scrapy.Request(self.url2.format(item["id"]),
                                         callback=self.parse_detail, meta={"item": item})
                yield request

        if res[0]['hasMorePages']:
            log.info("Next page request url = {}, page = {}".format(self.url, str(currentPage + 1)))
            yield scrapy.FormRequest(url=self.url,
                                     formdata={'page': str(currentPage + 1), 'show_sold_out': 'false', 'sortby': '2'},
                                     callback=self.parse)

    def parse_detail(self, response):
        item = response.meta["item"]
        res = response.body.decode()
        res = res.replace('true', 'True')
        res = res.replace('false', 'False')
        res = res.replace('null', 'None')
        res = eval(res)
        item["detail"] = res["data"]["description"]
        item["contact"] = res["data"]["contact"]
        # select field
        item_t = {}
        item_t["source"] = "ticketdee"
        item_t["id"] = item["id"]
        item_t["title"] = item["title"]
        item_t["detail"] = item["detail"]
        item_t["price"] = item["price"]
        item_t["contact"] = item["contact"]
        item_t["link"] = None
        yield item_t
