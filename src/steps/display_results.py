from typing import List

from prettytable import PrettyTable
import numpy as np

from src.models.owner import Owner
from src.models.trade import Trade


def display_results(trades: List[Trade], owners: List[Owner]) -> None:
    sorted_trades = sorted(
        trades,
        key=lambda t: np.mean([t.their_long_term_impact, t.my_long_term_impact]),
        reverse=True
    )
    print('\nTrades to consider (%s):' % len(trades))
    t = PrettyTable()
    t.field_names = ['Trade', 'For', 'With', 'Short-Term Impact', 'Long-Term Impact']
    t.align['Trade'] = 'l'
    t.align['For'] = 'l'
    t.align['With'] = 'l'
    t.align['Short-Term Impact'] = 'r'
    t.align['Long-Term Impact'] = 'r'
    for trade in sorted_trades:
        other_owner = next(o for o in owners if o.id == trade.their_player.owner_id)
        t.add_row([
            trade.my_player, trade.their_player, other_owner,
            '+%s, +%s' % (float(trade.their_short_term_impact), float(trade.my_short_term_impact)),
            '+%s, +%s' % (trade.their_long_term_impact, trade.my_long_term_impact)
        ])
    print(t)
    print('\n')
