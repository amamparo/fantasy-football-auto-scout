from os import environ
from typing import Dict

from dotenv import load_dotenv, find_dotenv

from src.constants import positions

load_dotenv(find_dotenv())

league_id: int = int(environ.get('LEAGUE_ID'))
season: int = int(environ.get('SEASON'))
request_cookie: str = environ.get('REQUEST_COOKIE')
num_weeks: int = int(environ.get('WEEKS'))
starters_by_position: Dict[str, int] = {
    position: int(environ.get(position))
    for position in positions
}
has_flex: bool = (environ.get('HAS_FLEX') or 'false').lower() == 'true'
