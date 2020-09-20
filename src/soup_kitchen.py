import requests
from bs4 import BeautifulSoup

from src.env import request_cookie, proxy_base_url


class SoupKitchen:
    @staticmethod
    def get(url_path: str) -> BeautifulSoup:
        return BeautifulSoup(
            requests.get('%s%s' % (proxy_base_url, url_path), headers={'cookie': request_cookie}).text,
            'lxml'
        )
