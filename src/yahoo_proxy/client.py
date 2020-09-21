from abc import ABC, abstractmethod

import requests

from src.env import RealEnv, Env


class YahooProxyClient(ABC):
    @abstractmethod
    def get(self, url_path: str) -> str:
        pass


class RealYahooProxyClient(YahooProxyClient):
    def __init__(self, env: Env = RealEnv()):
        self.__env = env

    def get(self, url_path: str) -> str:
        return requests.get(
            '%s%s' % (self.__env.proxy_base_url, url_path),
            headers={'cookie': self.__env.request_cookie}
        ).text
