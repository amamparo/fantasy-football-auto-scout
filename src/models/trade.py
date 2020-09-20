from typing import Optional, List

from src.models.player import Player


class Trade:
    def __init__(self, my_players: List[Player], their_players: List[Player], my_impact: int,
                 their_impact: int):
        self.__my_players = my_players
        self.__their_players = their_players
        self.__my_impact = my_impact
        self.__their_impact = their_impact
        self.__my_long_term_impact: Optional[float] = None
        self.__their_long_term_impact: Optional[float] = None

    @property
    def my_players(self) -> List[Player]:
        return self.__my_players

    @property
    def their_players(self) -> List[Player]:
        return self.__their_players

    @property
    def my_impact(self) -> int:
        return self.__my_impact

    @property
    def their_impact(self) -> int:
        return self.__their_impact

    @property
    def my_long_term_impact(self) -> float:
        return self.__my_long_term_impact

    @property
    def their_long_term_impact(self) -> float:
        return self.__their_long_term_impact

    def is_mutually_beneficial(self) -> bool:
        return self.__my_impact > 0 and self.__their_impact > 0
