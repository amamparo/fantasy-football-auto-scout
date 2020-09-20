from typing import Dict

from bs4 import BeautifulSoup

from src.env import league_id
from src.models.league_settings import LeagueSettings
from src.soup_kitchen import SoupKitchen


class LeagueSettingsScraper:
    def __init__(self, soup_kitchen: SoupKitchen = SoupKitchen()):
        self.__soup_kitchen = soup_kitchen

    def scrape(self) -> LeagueSettings:
        soup = self.__soup_kitchen.get('/f1/%s/settings' % league_id)

        playoffs_text = self.__get_table_text(soup, 'Playoffs:')
        num_weeks = int([x for x in playoffs_text.replace(',', '').split(' ') if x.isnumeric()][-1])

        roster_text = self.__get_table_text(soup, 'Roster Positions:')
        standard_positions = ['QB', 'WR', 'RB', 'TE', 'K', 'DEF']
        roster_positions = [x.strip() for x in roster_text.strip().split(',') if x.strip() in standard_positions]
        starters_by_position: Dict[str, int] = {
            position: len([x for x in roster_positions if x == position])
            for position in list(set(roster_positions))
        }
        return LeagueSettings(
            num_weeks,
            starters_by_position,
            'W/R/T' in roster_text
        )

    @staticmethod
    def __get_table_text(soup: BeautifulSoup, row_label: str) -> str:
        return next(
            x for x in soup.findAll('tr')
            if x.find('td') and x.find('td').text.strip().replace(u'\xa0', ' ') == row_label.strip()
        ).findAll('td')[-1].text.strip()