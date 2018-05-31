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


# c66-lifestyle-voucher
# c231-lifestyle-concert_ticket
# c232-lifestyle-show_ticket
class KaideeSpider(scrapy.Spider):
    name = "kaidee"

    def start_requests(self):
        if self.settings["ENABLE_NOTI_SLACK"]:
            response = SlackNotification.sendMsg(self.settings["SLACK_WEBHOOK_URL"], "Start Kaidee spider.")
            if response.status_code != 200:
                log.error("Cannot send notfication slack when open spider")
        self.keywords = self.settings["OTHER_SEARCH_KEYWORDS"]
        self.keywords.append(self.settings["MAIN_SEARCH_KEYWORD"])
        category = getattr(self, 'category', 'c66-lifestyle-voucher')
        if category is not None:
            url = 'https://www.kaidee.com/' + category + '/'
            log.info("Send request for Kaidee URL = {}".format(url))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.xpath("//a[@class='crow']"):
            title = item.xpath(".//h2/text()").extract_first()
            if TextUtility.find_in_text(title, self.keywords) >= 0:
                item = {
                    'source': 'kaidee',
                    'id': None,
                    'title': title,
                    'detail': None,
                    'price': item.xpath(".//p[contains(@class,'price')]//text()").extract_first(),
                    'contact': None,
                    'link': "https://www.kaidee.com" + item.xpath(".//@href").extract_first()
                }
                request = scrapy.Request(item["link"], callback=self.parse_detail, meta={"item": item})
                yield request
        next_page = response.xpath("//a[@class='nextPage']").xpath("@href").extract_first()
        if next_page is not None:
            log.info("Next page request url = {}".format(next_page))
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta["item"]
        item["id"] = response.xpath("(//span[@class='df-icon-information']//text())[2]").extract_first()
        item["detail"] = ''.join(response.xpath("//p[@class='ad-description-detail']//text()").extract())
        item["contact"] = response.xpath("//span[@id='phone-all']//text()").extract_first()
        yield item
