from typing import Optional

from src.models.player import Player


class Trade:
    def __init__(self, my_player: Player, their_player: Player, my_short_term_impact: int,
                 their_short_term_impact: int):
        self.__my_player = my_player
        self.__their_player = their_player
        self.__my_short_term_impact = my_short_term_impact
        self.__their_short_term_impact = their_short_term_impact
        self.__my_long_term_impact: Optional[float] = None
        self.__their_long_term_impact: Optional[float] = None

    @property
    def my_player(self) -> Player:
        return self.__my_player

    @property
    def their_player(self) -> Player:
        return self.__their_player

    @property
    def my_short_term_impact(self) -> int:
        return self.__my_short_term_impact

    @property
    def their_short_term_impact(self) -> int:
        return self.__their_short_term_impact

    @property
    def my_long_term_impact(self) -> float:
        return self.__my_long_term_impact

    @property
    def their_long_term_impact(self) -> float:
        return self.__their_long_term_impact

    def set_long_term_impacts(self, mine: float, theirs: float) -> None:
        self.__my_long_term_impact = mine
        self.__their_long_term_impact = theirs

    def is_mutually_beneficial_in_the_short_term(self) -> bool:
        return self.my_short_term_impact > 0 and self.their_short_term_impact > 0

    def is_mutually_beneficial_in_the_long_term(self) -> bool:
        return self.__my_long_term_impact >= 0 and self.__their_long_term_impact >= 0
