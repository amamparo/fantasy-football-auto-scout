from bs4 import BeautifulSoup

from src.yahoo_proxy.client import YahooProxyClient


class SoupKitchen:
    def __init__(self, yahoo_proxy_client: YahooProxyClient = YahooProxyClient()):
        self.__yahoo_proxy_client = yahoo_proxy_client

    def get(self, url_path: str) -> BeautifulSoup:
        return BeautifulSoup(self.__yahoo_proxy_client.get(url_path), 'lxml')
