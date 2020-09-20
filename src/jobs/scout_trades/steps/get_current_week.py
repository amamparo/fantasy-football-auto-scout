from src.env import league_id
from src.soup_kitchen import get_soup


def get_current_week() -> int:
    soup = get_soup('/f1/%s' % league_id)
    return int(soup.find('span', id='matchup_selectlist_nav').findAll('a')[1].text.strip().split(' ')[-1])