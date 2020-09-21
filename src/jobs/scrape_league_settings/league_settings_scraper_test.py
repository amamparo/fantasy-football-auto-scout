import random
from typing import Optional
from unittest import TestCase

from src.env import Env
from src.jobs.scrape_league_settings.league_settings_scraper import LeagueSettingsScraper
from src.models.league_settings import LeagueSettings
from src.soup_kitchen import SoupKitchen
from src.yahoo_proxy.client import YahooProxyClient


def mock_league_settings_scraper(html: str) -> LeagueSettingsScraper:
    random_league_id = random.randint(1, 1000)

    class FakeEnv(Env):
        @property
        def league_id(self) -> int:
            return random_league_id

        @property
        def request_cookie(self) -> str:
            pass

        @property
        def proxy_base_url(self) -> str:
            pass

        @property
        def proxy_port(self) -> Optional[int]:
            pass

    class FakeYahooProxyClient(YahooProxyClient):
        def get(self, url_path: str) -> str:
            if url_path != '/f1/%s/settings' % random_league_id:
                return 'Invalid League'
            return html

    soup_kitchen = SoupKitchen(FakeYahooProxyClient())
    return LeagueSettingsScraper(soup_kitchen, FakeEnv())


class LeagueSettingsScraperTest(TestCase):
    def test_base_case(self):
        league_settings: LeagueSettings = mock_league_settings_scraper('''
            <table>
                <tbody>
                    <tr>
                        <td>Playoffs:</td>
                        <td>Week 14, 15, and 16 (8 teams)</td>
                    </tr>
                    <tr>
                        <td>Roster Positions:</td>
                        <td>QB, WR, WR, RB, RB, TE, W/R/T, K, DEF, BN, BN, BN, BN, BN, BN, BN</td>
                    </tr>
                </tbody>
            </table>
        ''').scrape()
        self.assertEqual(16, league_settings.num_weeks)
        self.assertTrue(league_settings.has_flex)
        starters_by_position = league_settings.starters_by_position
        self.assertEqual(1, starters_by_position['QB'])
        self.assertEqual(2, starters_by_position['WR'])
        self.assertEqual(2, starters_by_position['RB'])
        self.assertEqual(1, starters_by_position['TE'])
        self.assertEqual(1, starters_by_position['K'])
        self.assertEqual(1, starters_by_position['DEF'])
