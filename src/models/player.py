from typing import Optional


class Player:
    def __init__(self, _id: int, name: str, team: str, position: str, projection: int, owner_id: int):
        self.__id = _id
        self.__name = name
        self.__team = team
        self.__position = position
        self.__projection = projection
        self.__owner_id = owner_id
        self.__z_score: Optional[float] = None

    def set_z_score(self, z_score: float) -> None:
        self.__z_score = z_score

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def team(self) -> str:
        return self.__team

    @property
    def position(self) -> str:
        return self.__position

    @property
    def projection(self) -> int:
        return self.__projection

    @property
    def owner_id(self) -> int:
        return self.__owner_id

    @property
    def z_score(self) -> float:
        return self.__z_score

    def __str__(self) -> str:
        return '%s %s (%s)' % (self.position, self.name, self.team)

    def __repr__(self) -> str:
        return self.__str__()


