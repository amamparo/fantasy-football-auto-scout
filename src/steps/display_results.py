from typing import List

from prettytable import PrettyTable, ALL
import numpy as np

from src.models.owner import Owner
from src.models.trade import Trade


def display_results(trades: List[Trade], owners: List[Owner]) -> None:
    sorted_trades = sorted(
        trades,
        key=lambda t: np.mean([t.their_impact, t.my_impact]),
        reverse=True
    )
    print('\nTrades to consider (%s):' % len(trades))
    t = PrettyTable(hrules=ALL)
    t.field_names = ['Trade', 'For', 'With', 'Their Impact', 'My Impact']
    t.align['Trade'] = 'l'
    t.align['For'] = 'l'
    t.align['With'] = 'l'
    t.align['Their Impact'] = 'r'
    t.align['My Impact'] = 'r'
    for trade in sorted_trades:
        other_owner = next(o for o in owners if o.id == trade.their_players[0].owner_id)
        t.add_row([
            '\n'.join(map(str, trade.my_players)), '\n'.join(map(str, trade.their_players)), other_owner,
            '+%s' % trade.their_impact, '+%s' % trade.my_impact
        ])
    print(t)
    print('\n')
