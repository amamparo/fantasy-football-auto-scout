from os import environ

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

league_id: int = int(environ.get('LEAGUE_ID'))
request_cookie: str = environ.get('REQUEST_COOKIE')
