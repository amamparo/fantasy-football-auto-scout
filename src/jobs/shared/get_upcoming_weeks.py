from typing import List

from src.env import league_id, num_weeks
from src.soup_kitchen import SoupKitchen


def get_upcoming_weeks(soup_kitchen: SoupKitchen) -> List[int]:
    soup = soup_kitchen.get('/f1/%s' % league_id)
    current_week = int(soup.find('span', id='matchup_selectlist_nav').findAll('a')[1].text.strip().split(' ')[-1])
    return list(range(current_week + 1, num_weeks + 1))
