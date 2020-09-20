import requests

from src.env import proxy_base_url, request_cookie


class YahooProxyClient:
    @staticmethod
    def get(url_path: str) -> str:
        return requests.get('%s%s' % (proxy_base_url, url_path), headers={'cookie': request_cookie}).text