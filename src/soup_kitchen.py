import random
import time
from os import path
from pathlib import Path
from typing import Optional, List, Tuple

import requests
from bs4 import BeautifulSoup

from src.constants import base_url
from src.env import request_cookie

last_http_request: Optional[float] = None
min_seconds_between_requests: float = 5
max_seconds_between_requests: float = 10


def __conditionally_sleep() -> None:
    if last_http_request is not None:
        seconds_since_last_http_request = time.time() - last_http_request
        randomized_throttle_buffer = random.uniform(min_seconds_between_requests, max_seconds_between_requests)
        sleep_time = max(randomized_throttle_buffer - seconds_since_last_http_request, 0)
        time.sleep(sleep_time)


def __update_last_http_request_time():
    global last_http_request
    last_http_request = time.time()


def __get_from_cache(cache_file_path: str) -> Optional[str]:
    if path.exists(cache_file_path):
        with open(cache_file_path) as cached_file:
            return cached_file.read()


def __cached_and_throttled_get(url: str, form_data: Optional[List[Tuple[str, any]]] = None) -> str:
    serialized_form_data = '&'.join(['%s=%s' % (key, val) for key, val in (form_data or [])])
    cache_dir = '.cache'
    Path(cache_dir).mkdir(exist_ok=True)
    cache_file_path = path.join(
        cache_dir,
        '%s%s.html' % (
            url.replace('/', ':'),
            '' if form_data is None else '__%s' % serialized_form_data
        )
    )
    cached_html = __get_from_cache(cache_file_path)
    if cached_html is not None:
        return cached_html
    __conditionally_sleep()
    requests_method = requests.post if form_data else requests.get
    html = requests_method(url, data=form_data, headers={'cookie': request_cookie}).text
    __update_last_http_request_time()
    with open(cache_file_path, 'w+') as cached_file:
        cached_file.write(html)
    return html


def get_soup(url_path: str, form_data: Optional[List[Tuple[str, any]]] = None) -> BeautifulSoup:
    return BeautifulSoup(__cached_and_throttled_get('%s%s' % (base_url, url_path), form_data), 'lxml')
