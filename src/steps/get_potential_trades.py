from itertools import product
from typing import List

from src.env import starters_by_position, has_flex
from src.models.owner import Owner
from src.models.player import Player
from src.models.trade import Trade


def get_potential_trades(owners: List[Owner], players: List[Player]) -> List[Trade]:
    potential_trades: List[Trade] = []
    my_roster = [p for p in players if p.owner_id == next(o for o in owners if o.is_current_user).id]

    for other_owner in [o for o in owners if not o.is_current_user]:
        their_roster = [p for p in players if p.owner_id == other_owner.id]
        for my_player, their_player in list(product(my_roster, their_roster)):
            if my_player.position == their_player.position:
                continue
            potential_trades.append(Trade(
                [my_player],
                [their_player],
                __evaluate_short_term_impact_of_trade(my_roster, [my_player], [their_player]),
                __evaluate_short_term_impact_of_trade(their_roster, [their_player], [my_player])
            ))
    return [t for t in potential_trades if t.is_mutually_beneficial()]


def __evaluate_short_term_impact_of_trade(roster: List[Player], players_out: List[Player],
                                          players_in: List[Player]) -> int:
    roster_after_trade = [p for p in roster if p.id not in map(lambda x: x.id, players_out)] + players_in
    return __get_projected_total_points(roster_after_trade) - __get_projected_total_points(roster)


def __get_projected_total_points(roster: List[Player]) -> int:
    weeks = sorted(list(set([week for player in roster for week in player.weekly_projections.keys()])))
    positions = list(set(map(lambda p: p.position, roster)))
    total_points: int = 0
    for week in weeks:
        sorted_roster = sorted(roster, key=lambda p: p.get_weekly_projection(week), reverse=True)
        starting_lineup: List[Player] = []
        for position in positions:
            starting_lineup.extend(
                [p for p in sorted_roster if p.position == position][:starters_by_position[position]]
            )
        if has_flex:
            starting_lineup.append(next(
                p for p in sorted_roster
                if p.position in ['WR', 'RB', 'TE'] and p.id not in map(lambda x: x.id, starting_lineup)
            ))
        total_points += sum(map(lambda p: p.get_weekly_projection(week), starting_lineup))
    return total_points
