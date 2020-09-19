from itertools import product
from typing import List, Tuple

from tqdm import tqdm

from src.env import league_id
from src.models.owner import Owner
from src.models.player import Player
from src.models.trade import Trade
from src.soup_kitchen import get_soup


def evaluate_and_shortlist_trades(owners: List[Owner], players: List[Player]) -> List[Trade]:
    relevant_players = [p for p in players if p.position.lower() not in ['k', 'def']]
    me = next(o for o in owners if o.is_current_user)
    my_players = [p for p in relevant_players if p.owner_id == me.id]
    prospective_trade_partners = [o for o in owners if o.is_active and not o.is_current_user]
    prospects = [p for p in relevant_players if p.owner_id in map(lambda o: o.id, prospective_trade_partners)]
    trade_pairs: List[Tuple[Player, Player]] = list(product(my_players, prospects))
    trade_pairs = [
        (my_player, their_player)
        for my_player, their_player in trade_pairs
        if my_player.position != their_player.position and abs(my_player.z_score - their_player.z_score) <= 0.5
    ]
    trades: List[Trade] = []
    for my_player, their_player in tqdm(trade_pairs):
        trades.append(__evaluate_trade(my_player, their_player))
    return sorted([t for t in trades if t.is_mutually_beneficial()], key=lambda t: t.impact_to_me, reverse=True)


def __evaluate_trade(my_player: Player, their_player: Player) -> Trade:
    soup = get_soup(
        '/f1/%s/%s/proposetrade' % (league_id, my_player.owner_id),
        {
            'mid2': their_player.owner_id,
            'tpids[]': [my_player.id],
            'tpids2[]': [their_player.id],
            'evaluate': 'evaluate trade'
        }
    )
    impact_table = soup.find('table', id='statTable2')
    impact_to_me_row, impact_to_them_row = impact_table.find('tbody').findAll('tr')

    def __parse_impact(td_text: str) -> float:
        if td_text.lower() in ['even', '-']:
            return 0
        return float(td_text)

    impact_to_me = __parse_impact(impact_to_me_row.findAll('td')[-1].text)
    impact_to_them = __parse_impact(impact_to_them_row.findAll('td')[-1].text)
    return Trade(my_player, their_player, impact_to_me, impact_to_them)
