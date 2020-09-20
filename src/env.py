from os import environ
from typing import Dict

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

league_id: int = int(environ.get('LEAGUE_ID'))
season: int = int(environ.get('SEASON'))
request_cookie: str = environ.get('REQUEST_COOKIE')
QB: int = int(environ.get('QB'))
WR: int = int(environ.get('WR'))
RB: int = int(environ.get('RB'))
TE: int = int(environ.get('TE'))
starters_by_position: Dict[str, int] = {
    position: int(environ.get(position))
    for position in ['QB', 'WR', 'RB', 'TE']
}
has_flex: bool = (environ.get('HAS_FLEX') or 'false').lower() == 'true'
