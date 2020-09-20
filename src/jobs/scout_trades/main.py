from src.jobs.shared.get_upcoming_weeks import get_upcoming_weeks
from src.jobs.scout_trades.steps.display_results import display_results
from src.jobs.scout_trades.steps.get_potential_trades import get_potential_trades
from src.jobs.scout_trades.steps.get_owners import get_owners
from src.jobs.scout_trades.steps.get_rostered_players import get_rostered_players
from src.soup_kitchen import SoupKitchen


def main():
    soup_kitchen = SoupKitchen()
    owners = get_owners(soup_kitchen)
    players = get_rostered_players(owners, soup_kitchen)
    trades = get_potential_trades(owners, players)
    display_results(trades, owners)


if __name__ == '__main__':
    main()
