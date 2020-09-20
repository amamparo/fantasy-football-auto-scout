from itertools import product
from typing import List

from tqdm import tqdm

from src.env import league_id
from src.models.owner import Owner
from src.models.player import Player
from src.soup_kitchen import get_soup

num_weeks_to_look_ahead = 4


def get_rostered_players(owners: List[Owner], current_week: int) -> List[Player]:
    print('\nLoading rosters...')
    players: List[Player] = []
    weeks = [current_week + 1 + i for i in range(num_weeks_to_look_ahead)]
    for owner, week in tqdm(list(product(owners, weeks))):
        soup = get_soup('/f1/%s/%s?week=%s&stat1=P&stat2=PW' % (league_id, owner.id, week))
        table = soup.find('table', id='statTable0')
        for tr in table.find('tbody').findAll('tr'):
            info = tr.find('div', {'class': 'ysf-player-name'})
            _id = int(info.find('a')['href'].split('/')[-1])
            player = next((p for p in players if p.id == _id), None)
            if not player:
                name = info.find('a').text
                team, position = [token.strip() for token in info.find('span').text.split('-')]
                players.append(Player(_id, name, team, position, owner.id))
            bolded_trs = tr.findAll('span', {'class': 'Fw-b'})
            projection = int(bolded_trs[-1].text.strip()) if bolded_trs else 0
            next(p for p in players if p.id == _id).set_weekly_projection(week, projection)
    return players
