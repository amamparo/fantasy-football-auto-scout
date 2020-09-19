from typing import List

import numpy as np
from tqdm import tqdm

from src.env import league_id, season
from src.models.owner import Owner
from src.models.player import Player
from src.soup_kitchen import get_soup


def get_rostered_players(owners: List[Owner]) -> List[Player]:
    players: List[Player] = []
    for owner in tqdm(owners):
        soup = get_soup('/f1/%s/%s?stat1=P&stat2=PSR_%s' % (league_id, owner.id, season))
        table = soup.find('table', id='statTable0')
        for tr in table.find('tbody').findAll('tr'):
            info = tr.find('div', {'class': 'ysf-player-name'})
            _id = int(info.find('a')['href'].split('/')[-1])
            name = info.find('a').text
            team, position = [token.strip() for token in info.find('span').text.split('-')]
            projection = int(tr.findAll('span', {'class': 'Fw-b'})[-1].text.strip())
            players.append(Player(_id, name, team, position, projection, owner.id))

    for position in list(set([p.position for p in players])):
        position_players = [p for p in players if p.position == position]
        mean_projection = float(np.mean([p.projection for p in position_players]))
        std_projection = float(np.std([p.projection for p in position_players]))
        for player in position_players:
            player.set_z_score((player.projection - mean_projection) / std_projection)

    return players