import scrapy

from oreilly import settings


class CatalogueSpider(scrapy.Spider):
    name = "catalogue"

    def start_requests(self):
        url = settings.CATALOGUE_URL
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.json()
        for record in data["results"]:
            yield record

        if data.get("next", None):
            yield scrapy.Request(url=data["next"], callback=self.parse)
