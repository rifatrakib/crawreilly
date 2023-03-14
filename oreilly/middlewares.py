from datetime import datetime
from pathlib import Path

from scrapy import signals

from services.credentials import prepare_json_credentials, read_json_credentials
from services.logger import log_writer


class OreillySpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        location = "logs/meta"
        Path(location).mkdir(parents=True, exist_ok=True)
        file_path = f"{location}/{spider.name}.log"
        string = (
            f"ERROR: {str(exception)} occurred for "
            f"{response.request.url} while running {spider.name} spider "
            f"at {datetime.utcnow().isoformat()}\n"
        )
        log_writer(file_path, string)

    def process_start_requests(self, start_requests, spider):
        location = "logs/meta"
        Path(location).mkdir(parents=True, exist_ok=True)

        for r in start_requests:
            file_path = f"{location}/{spider.name}.log"
            string = (
                f"INFO: {r.method} request fired for {spider.name} with {r.url} at {datetime.utcnow().isoformat()}\n"
            )
            log_writer(file_path, string)
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class OreillyDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if request.headers:
            return None

        location = "keys/credentials"
        Path(location).mkdir(parents=True, exist_ok=True)

        if not Path(f"{location}/{spider.name}.sh").exists():
            prepare_json_credentials(spider.name)

        credentials = read_json_credentials(spider.name)

        for key, value in credentials["headers"].items():
            request.headers[key] = value

        for key, value in credentials["cookies"].items():
            request.cookies[key] = value

        request.headers["content-type"] = "application/json"

        if spider.name != "auth":
            credentials = read_json_credentials(spider.name)
            for key, value in credentials["headers"].items():
                if key not in request.headers:
                    request.headers[key] = value
            for key, value in credentials["cookies"].items():
                if key not in request.cookies:
                    request.cookies[key] = value

        return None

    def process_response(self, request, response, spider):
        location = "logs/fails"
        Path(location).mkdir(parents=True, exist_ok=True)

        if (
            response.status == 200
            and response.headers.get("content-type") == "application/json"
            and "success" in response.json()
            and not response.json()["success"]
        ):
            file_path = f"{location}/{spider.name}.log"
            string = f"request to {request.url} failed with {response.json()} at {datetime.utcnow().isoformat()}\n"
            log_writer(file_path, string)

        return response

    def process_exception(self, request, exception, spider):
        location = "logs/fails"
        Path(location).mkdir(parents=True, exist_ok=True)

        file_path = f"{location}/{spider.name}.log"
        string = f"ERROR: request to {request.url} failed with {str(exception)} at {datetime.utcnow().isoformat()}\n"
        log_writer(file_path, string)

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
