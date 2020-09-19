from os import environ
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

league_id: int = int(environ.get('LEAGUE_ID'))
season: int = int(environ.get('SEASON'))
request_cookie: str = environ.get('REQUEST_COOKIE')
