import scrapy


class AuthSpider(scrapy.Spider):
    name = "auth"
    custom_settings = {
        "SPIDER_MIDDLEWARES": {},
        "DOWNLOADER_MIDDLEWARES": {},
        "ITEM_PIPELINES": {},
    }

    def start_requests(self):
        with open("keys/raw/auth.sh") as reader:
            curl = reader.read()
        yield scrapy.Request.from_curl(curl)

    def parse(self, response):
        print(response.json())
        print(response.headers)
