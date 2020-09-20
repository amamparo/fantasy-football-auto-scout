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
    my_players = trade.my_players
    their_players = trade.their_players
    form_data = [
        ('mid2', their_players[0].owner_id),
        ('evaluate', 'evaluate trade')
    ]
    form_data.extend([('typids[]', x.id) for x in my_players])
    form_data.extend([('typids2[]', x.id) for x in their_players])
    soup = get_soup('/f1/%s/%s/proposetrade' % (league_id, my_players[0].owner_id), form_data)
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
