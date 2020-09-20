from src.env import league_id
from src.jobs.scout_trades.steps import get_current_week


def main():
    current_week = get_current_week()
    soup = get_soup('/f1/%s/players?status=T&pos=%s&stat1=S_PW_%s' % (league_id, 'pos', 'week'))


if __name__ == '__main__':
    main()
