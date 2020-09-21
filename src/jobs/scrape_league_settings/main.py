from src.jobs.scrape_league_settings.league_settings_scraper import LeagueSettingsScraper


def lambda_handler(event: dict = None, context: any = None) -> None:
    league_settings = LeagueSettingsScraper().scrape()
    print(league_settings.serialize())
