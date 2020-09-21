import logging
import random
import time
import traceback
from threading import Lock

import requests
from flask import Flask, Response, request

from src.constants import base_url
from src.env import RealEnv

logger = logging.getLogger('yahoo-proxy-server')
logger.setLevel(logging.INFO)

app = Flask(__name__)

last_http_request: float = time.time()
min_seconds_between_requests: float = 5
max_seconds_between_requests: float = 10

lock = Lock()


def __throttled_get(url_path: str, cookie: str) -> str:
    global last_http_request
    with lock:
        if last_http_request is not None:
            seconds_since_last_http_request = time.time() - last_http_request
            randomized_throttle_buffer = random.uniform(min_seconds_between_requests, max_seconds_between_requests)
            sleep_time = max(randomized_throttle_buffer - seconds_since_last_http_request, 0)
            time.sleep(sleep_time)

        html = requests.get('%s%s' % (base_url, url_path), headers={'cookie': cookie}).text
        last_http_request = time.time()
        return html


@app.errorhandler(500)
def five_hundred_error(e):
    logger.error('an error happened', exc_info=e)
    return Response(traceback.format_exc(), status=500, mimetype='application/text')


@app.route('/')
def health_check():
    return 'hello world'


@app.route('/<path:ignored>')
def forward_to_yahoo(ignored):
    cookie: str = request.headers.get('cookie')
    if not cookie:
        return 'Missing Cookie', 401
    return __throttled_get(request.full_path, cookie), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=RealEnv().proxy_port, debug=True, threaded=False)
