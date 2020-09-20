from typing import Optional

from bs4 import BeautifulSoup

from src.yahoo_http_client import YahooHttpClient

last_http_request: Optional[float] = None
min_seconds_between_requests: float = 5
max_seconds_between_requests: float = 10


class SoupKitchen:
    def __init__(self, yahoo_http_client: YahooHttpClient = YahooHttpClient()):
        self.__yahoo_http_client = yahoo_http_client

    def get(self, url_path: str) -> BeautifulSoup:
        return BeautifulSoup(self.__yahoo_http_client.get(url_path), 'lxml')
