from src.env import league_id
from src.jobs.shared import get_upcoming_weeks


def main():
    current_week = get_upcoming_weeks()
    soup = get_soup('/f1/%s/players?status=T&pos=%s&stat1=S_PW_%s' % (league_id, 'pos', 'week'))


if __name__ == '__main__':
    main()
