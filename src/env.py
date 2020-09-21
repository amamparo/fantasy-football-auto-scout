from abc import ABC, abstractmethod
from os import environ
from typing import Optional

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Env(ABC):
    @property
    @abstractmethod
    def league_id(self) -> int:
        pass

    @property
    @abstractmethod
    def request_cookie(self) -> str:
        pass

    @property
    @abstractmethod
    def proxy_base_url(self) -> str:
        pass

    @property
    @abstractmethod
    def proxy_port(self) -> Optional[int]:
        pass


class RealEnv(Env):
    @property
    def league_id(self) -> int:
        return int(environ.get('LEAGUE_ID'))

    @property
    def request_cookie(self) -> str:
        return environ.get('REQUEST_COOKIE')

    @property
    def proxy_base_url(self) -> str:
        return environ.get('PROXY_BASE_URL')

    @property
    def proxy_port(self) -> Optional[int]:
        key = 'PROXY_PORT'
        return int(environ.get(key)) if environ.get(key) else None
