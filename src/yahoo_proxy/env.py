from os import environ

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

port: int = int(environ.get('PROXY_PORT'))
