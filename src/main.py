from prettytable import PrettyTable

from src.evaluate_and_shortlist_trades import evaluate_and_shortlist_trades
from src.get_owners import get_owners
from src.get_rostered_players import get_rostered_players


def main():
    owners = get_owners()

    print('\nGetting player info...')
    players = get_rostered_players(owners)
    print('\nGot %s rostered players' % len(players))

    print('\nGenerating trades shortlist...')
    trades = evaluate_and_shortlist_trades(owners, players)

    print('\nTrades to consider (%s):' % len(trades))
    t = PrettyTable()
    t.field_names = ['Trade', 'For', 'With', 'Their Impact', 'My Impact']
    for trade in trades:
        other_owner = next(o for o in owners if o.id == trade.their_player.owner_id)
        t.add_row([trade.my_player, trade.their_player, other_owner, trade.impact_to_them, trade.impact_to_me])
    print(t)


if __name__ == '__main__':
    main()
