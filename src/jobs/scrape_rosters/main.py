from itertools import product
from typing import List

from bs4 import BeautifulSoup
from tqdm import tqdm

from src.constants import positions
from src.env import league_id
from src.jobs.shared.get_upcoming_weeks import get_upcoming_weeks
from src.soup_kitchen import SoupKitchen


def scrape_projections_for_rostered_players(soup_kitchen: SoupKitchen) -> None:
    soups: List[BeautifulSoup] = []
    for position, week in tqdm(list(product(positions, get_upcoming_weeks(soup_kitchen)))):
        soup = soup_kitchen.get('/f1/%s/players?status=T&pos=%s&stat1=S_PW_%s' % (league_id, position, week))
        soups.append(soup)
        next_25_link = soup.find('a', text='Next 25')
        while next_25_link:
            soup = soup_kitchen.get(next_25_link['href'])
            soups.append(soup)
            next_25_link = soup.find('a', text='Next 25')
    print(len(soups))


def main():
    soup_kitchen = SoupKitchen()
    scrape_projections_for_rostered_players(soup_kitchen)


if __name__ == '__main__':
    main()
