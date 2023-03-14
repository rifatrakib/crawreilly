import json
from datetime import datetime
from pathlib import Path

import scrapy

from services.credentials import prepare_json_credentials, read_json_credentials


class BookSpider(scrapy.Spider):
    name = "book"
    base_url = "https://learning.oreilly.com"

    def get_directory(self, kwargs):
        root_directory = "data/resources"
        category = kwargs.get("category")
        name = kwargs.get("name")
        page = kwargs.get("page", None)

        directory = f"{root_directory}/{category}/{name}"
        if page:
            directory = f"{root_directory}/{category}/{name}/{page}"

        Path(directory).mkdir(parents=True, exist_ok=True)
        return directory

    def start_requests(self):
        current_date = datetime.utcnow().date().isoformat()
        with open(f"data/json/catalogue-{current_date}.json") as reader:
            catalogue = json.loads(reader.read())

        metadata = {
            "category": catalogue[0]["topics_payload"][0]["name"],
            "name": catalogue[0]["title"],
        }
        yield scrapy.Request(
            url=f"{self.base_url}/api/v2/epub-chapters/{catalogue[0]['archive_id']}-/cover.html/",
            callback=self.parse_resources,
            cb_kwargs=metadata,
        )

    def parse_resources(self, response, **kwargs):
        data = {**response.json(), **kwargs}
        yield data
        assets = data["related_assets"]
        html_files = assets["html_files"]
        stylesheets = assets["stylesheets"]
        images = assets["images"]

        for html_link in html_files:
            yield scrapy.Request(
                url=html_link,
                callback=self.parse_htmls,
                cb_kwargs=kwargs,
            )

        for css_link in stylesheets:
            yield scrapy.Request(
                url=css_link,
                callback=self.parse_styles,
                cb_kwargs=kwargs,
            )

        location = "keys/credentials"
        Path(location).mkdir(parents=True, exist_ok=True)

        if not Path(f"{location}/image.sh").exists():
            prepare_json_credentials("image")

        credentials = read_json_credentials("image")
        image_headers = {}
        image_cookies = {}
        for key, value in credentials["headers"].items():
            if key != "Referer":
                image_headers[key] = value
            else:
                image_headers[key] = response.url

        for key, value in credentials["cookies"].items():
            image_cookies[key] = value

        page = response.url.rsplit("/", 2)[1].split(".")[0]
        for images in images:
            yield scrapy.Request(
                url=images,
                callback=self.parse_images,
                cb_kwargs={**kwargs, "page": page},
                headers=image_headers,
                cookies=image_cookies,
            )

        root_url = response.url.rsplit("/", 2)[0]
        next_chapter = assets.get("next_chapter", None)
        if next_chapter:
            next_item = next_chapter["url"].rsplit("/", 1)[-1]
            yield scrapy.Request(
                url=f"{root_url}/{next_item}/",
                callback=self.parse_resources,
                cb_kwargs=kwargs,
            )

    def parse_htmls(self, response, **kwargs):
        location = self.get_directory(kwargs)
        file_name = response.url.rsplit("/")[-1]
        html = response.body

        with open(f"{location}/{file_name}", "wb") as writer:
            writer.write(html)

    def parse_styles(self, response, **kwargs):
        location = self.get_directory(kwargs)
        file_name = response.url.rsplit("/")[-1]
        styles = response.body

        with open(f"{location}/{file_name}", "wb") as writer:
            writer.write(styles)

    def parse_images(self, response, **kwargs):
        location = self.get_directory(kwargs)
        file_name = response.url.rsplit("/")[-1]
        image = response.body

        with open(f"{location}/{file_name}", "wb") as writer:
            writer.write(image)
