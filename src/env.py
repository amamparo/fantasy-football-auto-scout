from os import environ
from typing import Optional

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

league_id: int = int(environ.get('LEAGUE_ID'))
request_cookie: str = environ.get('REQUEST_COOKIE')
proxy_base_url: str = environ.get('PROXY_BASE_URL')
proxy_port: Optional[int] = int(environ.get('PROXY_PORT')) if environ.get('PROXY_PORT') else None
