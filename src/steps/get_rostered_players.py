from itertools import product
from typing import List

from tqdm import tqdm

from src.env import league_id, num_weeks
from src.models.owner import Owner
from src.models.player import Player
from src.soup_kitchen import SoupKitchen


def get_rostered_players(owners: List[Owner], current_week: int, soup_kitchen: SoupKitchen) -> List[Player]:
    print('\nLoading rosters...')
    players: List[Player] = []
    weeks = range(current_week + 1, num_weeks + 1)
    for owner, week in tqdm(list(product(owners, weeks))):
        soup = soup_kitchen.get('/f1/%s/%s?week=%s&stat1=P&stat2=PW' % (league_id, owner.id, week))
        for table_id in ['statTable0', 'statTable1', 'statTable2']:
            table = soup.find('table', id=table_id)
            for tr in table.find('tbody').findAll('tr'):
                info = tr.find('div', {'class': 'ysf-player-name'})
                _id = [t for t in info.find('a')['href'].split('/') if t != ''][-1]
                player = next((p for p in players if p.id == _id), None)
                if not player:
                    name = info.find('a').text
                    team, position = [token.strip() for token in info.find('span').text.split('-')]
                    players.append(Player(_id, name, team, position, owner.id))
                bolded_trs = tr.findAll('span', {'class': 'Fw-b'})
                projection = int(float(bolded_trs[-1].text.strip()))if bolded_trs else 0
                next(p for p in players if p.id == _id).set_weekly_projection(week, projection)
    return players
