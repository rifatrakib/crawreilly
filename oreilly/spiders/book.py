import json
from datetime import datetime

import scrapy


class BookSpider(scrapy.Spider):
    name = "book"
    base_url = "https://learning.oreilly.com"

    def start_requests(self):
        current_date = datetime.utcnow().date().isoformat()
        with open(f"data/json/catalogue-{current_date}.json") as reader:
            catalogue = json.loads(reader.read())

        yield scrapy.Request(
            url=f"{self.base_url}/api/v2/epub-chapters/{catalogue[0]['archive_id']}-/cover.html/",
            callback=self.parse_resources,
        )

    def parse_resources(self, response):
        data = response.json()
        yield data
        assets = data["related_assets"]
        html_files = assets["html_files"]
        stylesheets = assets["stylesheets"]
        images = assets["images"]

        for html_link in html_files:
            yield scrapy.Request(url=html_link, callback=self.parse_htmls)

        for css_link in stylesheets:
            yield scrapy.Request(url=css_link, callback=self.parse_styles)

        for images in images:
            yield scrapy.Request(url=images, callback=self.parse_images)

        root_url = response.url.rsplit("/", 2)[0]
        next_chapter = assets.get("next_chapter", None)
        if next_chapter:
            next_item = next_chapter["url"].rsplit("/", 1)[-1]
            yield scrapy.Request(
                url=f"{root_url}/{next_item}/",
                callback=self.parse_resources,
            )

    def parse_htmls(self, response):
        html = response.body.decode("utf-8")
        with open("data/cover.html", "w") as writer:
            writer.write(html)

    def parse_styles(self, response):
        styles = response.body.decode("utf-8")
        with open("data/styles.css", "w") as writer:
            writer.write(styles)

    def parse_images(self, response):
        image = response.body
        with open("data/image.png", "wb") as writer:
            writer.write(image)
