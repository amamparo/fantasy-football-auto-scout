from typing import List

from src.env import league_id
from src.models.owner import Owner
from src.soup_kitchen import get_soup


def get_owners() -> List[Owner]:
    soup = get_soup('/f1/%s' % league_id)
    standings_table = soup.find('table', id='standingstable')
    trs = standings_table.find('tbody').findAll('tr')
    owners: List[Owner] = []
    for tr in trs:
        owner_id = int(tr['data-target'].split('/')[-1])
        tds = tr.findAll('td')
        owner_name = tds[1].text.strip()
        moves_text: str = tds[-1].text
        is_active = moves_text.isnumeric() and int(moves_text) > 0
        is_current_user = 'Selected' in tr['class']
        owners.append(Owner(owner_id, owner_name, is_active, is_current_user))
    return owners