from src.steps.get_current_week import get_current_week
from src.steps.display_results import display_results
from src.steps.get_potential_trades import get_potential_trades
from src.steps.get_owners import get_owners
from src.steps.get_rostered_players import get_rostered_players
from src.soup_kitchen import SoupKitchen


def main():
    soup_kitchen = SoupKitchen()
    owners = get_owners(soup_kitchen)
    current_week = get_current_week(soup_kitchen)
    players = get_rostered_players(owners, current_week, soup_kitchen)
    trades = get_potential_trades(owners, players)
    display_results(trades, owners)


if __name__ == '__main__':
    main()
