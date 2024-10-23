import scrapy


class SpiderToscrapeSpider(scrapy.Spider):
    name = "spider_toscrape"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        pass
