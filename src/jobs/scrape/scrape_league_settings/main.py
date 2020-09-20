from src.jobs.scrape.scrape_league_settings.league_settings_scraper import LeagueSettingsScraper


def scrape_league_settings():
    league_settings = LeagueSettingsScraper().scrape()
    print(league_settings.serialize())


if __name__ == '__main__':
    scrape_league_settings()
