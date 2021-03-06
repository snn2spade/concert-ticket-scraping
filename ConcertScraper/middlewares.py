# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.exceptions import IgnoreRequest
import time
import logging
import os.path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

log = logging.getLogger(__name__)


class FacebookDownloaderMiddleware(object):

    def process_request(self, request, spider):
        FACEBOOK_USER = spider.settings["FACEBOOK_USER"]
        FACEBOOK_PASS = spider.settings["FACEBOOK_PASS"]
        SCROLL_PAUSE_TIME = spider.settings["FACEBOOK_SCROLL_PAUSE_TIME"]
        CHROME_DRVER_PATH = spider.settings["CHROME_DRIVER_PATH"]
        SELENIUM_REMOTE_URL = spider.settings["SELENIUM_REMOTE_URL"]
        SELENIUM_USING_REMOTE = spider.settings["SELENIUM_USING_REMOTE"]
        if not request.meta.get("facebook"):
            raise IgnoreRequest("Not facebook request")
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('headless')
        if SELENIUM_USING_REMOTE:
            self.browser = webdriver.Remote(command_executor=SELENIUM_REMOTE_URL,
                                            desired_capabilities=chrome_options.to_capabilities())
        else:
            if os.path.isfile(CHROME_DRVER_PATH):
                log.info("Found chrome driver file")
            else:
                log.error("Cannot access chrome driver file")
            self.browser = webdriver.Chrome(executable_path=CHROME_DRVER_PATH,
                                            chrome_options=chrome_options)
        self.browser.implicitly_wait(10)  # seconds
        self.browser.maximize_window()
        self.browser.get('https://www.facebook.com')
        email_input = self.browser.find_element(By.XPATH, "//input[@type='email']")
        email_input.clear()
        email_input.send_keys(FACEBOOK_USER)
        password_input = self.browser.find_element(By.XPATH, "//input[@type='password']")
        password_input.clear()
        password_input.send_keys(FACEBOOK_PASS)
        login_button = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        login_button.click()
        log.info("Facebook Downloader Middleware PROCESS REQUEST URL: {}".format(request.url))

        self.browser.get(request.url)

        # Get scroll height
        next_height = 500
        while True:
            self.browser.execute_script("window.scrollTo(0, {});".format(next_height))
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            max_height = self.browser.execute_script("return document.body.scrollHeight")
            log.info("Scroll to {}, max height = {} ".format(next_height, max_height))
            if next_height >= max_height:
                break
            next_height += 500

        time.sleep(SCROLL_PAUSE_TIME)
        response = HtmlResponse(self.browser.current_url, body=self.browser.page_source, encoding='utf-8')
        self.browser.quit()
        return response


class ConcertScraperSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ConcertScraperExtractorDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
