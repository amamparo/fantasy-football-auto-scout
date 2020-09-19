from src.models.player import Player


class Trade:
    def __init__(self, my_player: Player, their_player: Player, impact_to_me: float, impact_to_them: float):
        self.__my_player = my_player
        self.__their_player = their_player
        self.__impact_to_me = impact_to_me
        self.__impact_to_them = impact_to_them

    @property
    def my_player(self) -> Player:
        return self.__my_player

    @property
    def their_player(self) -> Player:
        return self.__their_player

    @property
    def impact_to_me(self) -> float:
        return self.__impact_to_me

    @property
    def impact_to_them(self) -> float:
        return self.__impact_to_them

    def is_mutually_beneficial(self) -> bool:
        return self.impact_to_me > 0 and self.impact_to_them > 0
