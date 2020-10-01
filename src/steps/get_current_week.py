from src.env import league_id
from src.soup_kitchen import SoupKitchen


def get_current_week(soup_kitchen: SoupKitchen) -> int:
    soup = soup_kitchen.get('/f1/%s' % league_id)
    return int(soup.find('span', id='matchup_selectlist_nav').findAll('a')[1].text.strip().split(' ')[-1])
