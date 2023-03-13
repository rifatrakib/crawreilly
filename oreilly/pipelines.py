import json
from datetime import datetime
from pathlib import Path

from itemadapter import ItemAdapter
from scrapy import signals
from scrapy.exporters import CsvItemExporter


class CSVPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        scraping_date = datetime.utcnow().date().isoformat()
        location = "data/csv"
        Path(location).mkdir(parents=True, exist_ok=True)

        self.filename = f"{spider.name}-{scraping_date}.csv"
        self.file = open(f"{location}/{self.filename}", "w+b")
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        item_data = {}
        for key, value in ItemAdapter(item).asdict().items():
            if isinstance(value, str):
                value = value.replace("\n", " ").strip()
            item_data[key] = value
        self.exporter.export_item(item_data)
        return item


class JSONPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        scraping_date = datetime.utcnow().date().isoformat()
        location = "data/json"
        Path(location).mkdir(parents=True, exist_ok=True)

        self.filename = f"{spider.name}-{scraping_date}.json"
        self.file = open(f"{location}/{self.filename}", "w")
        header = "[\n"
        self.file.write(header)

    def spider_closed(self, spider):
        footer = "]\n"
        self.file.write(footer)
        self.file.close()

        with open(f"data/json/{self.filename}", "r") as reader:
            data = reader.read()

        data = data.rpartition(",")
        data = data[0] + data[-1]
        data = json.loads(data)
        with open(f"data/json/{self.filename}", "w") as writer:
            writer.write(json.dumps(data, indent=4))

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        line = json.dumps(data, indent=4) + ",\n"
        self.file.write(line)
        return item


class JSONLinesPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        scraping_date = datetime.utcnow().date().isoformat()
        location = "data/jsonline"
        Path(location).mkdir(parents=True, exist_ok=True)

        self.filename = f"{spider.name}-{scraping_date}.jl"
        self.file = open(f"{location}/{self.filename}", "w")

    def spider_closed(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
