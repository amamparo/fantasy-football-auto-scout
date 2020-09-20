from src.jobs.scout_trades.steps.get_current_week import get_current_week
from src.jobs.scout_trades.steps.display_results import display_results
from src.jobs.scout_trades.steps.get_potential_trades import get_potential_trades
from src.jobs.scout_trades.steps.get_owners import get_owners
from src.jobs.scout_trades.steps.get_rostered_players import get_rostered_players


def main():
    owners = get_owners()
    current_week = get_current_week()
    players = get_rostered_players(owners, current_week)
    trades = get_potential_trades(owners, players)
    display_results(trades, owners)


if __name__ == '__main__':
    main()
