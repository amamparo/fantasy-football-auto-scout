import random
import time
from typing import Optional

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


def get_soup(url_path: str, post_data: Optional[dict] = None) -> BeautifulSoup:
    __conditionally_sleep()
    url = '%s%s' % (base_url, url_path)
    request_method = requests.post if post_data is not None else requests.get
    soup = BeautifulSoup(request_method(url, post_data, headers={'cookie': request_cookie}).text, 'lxml')
    __update_last_http_request_time()
    return soup
