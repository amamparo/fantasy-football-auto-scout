from typing import List, cast

from tqdm import tqdm

from src.env import league_id
from src.models.trade import Trade
from src.soup_kitchen import get_soup


def evaluate_potential_trades(potential_trades: List[Trade]) -> List[Trade]:
    print('\nEvaluating potential trades...')
    trades: List[Trade] = []
    for potential_trade in cast(List[Trade], tqdm(potential_trades)):
        trades.append(__evaluate_trade(potential_trade))
    return [t for t in trades if t.is_mutually_beneficial_in_the_long_term()]


def __evaluate_trade(trade: Trade) -> Trade:
    my_player = trade.my_player
    their_player = trade.their_player
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
    trade.set_long_term_impacts(impact_to_me, impact_to_them)
    return trade
