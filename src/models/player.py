from typing import Optional, Dict


class Player:
    def __init__(self, _id: int, name: str, team: str, position: str, owner_id: int):
        self.__id = _id
        self.__name = name
        self.__team = team
        self.__position = position
        self.__owner_id = owner_id
        self.__weekly_projections: Dict[int, int] = {}

    def set_weekly_projection(self, week: int, projection: int) -> None:
        self.__weekly_projections[week] = projection

    def get_weekly_projection(self, week: int) -> Optional[int]:
        return self.__weekly_projections.get(week)

    @property
    def weekly_projections(self) -> Dict[int, int]:
        return self.__weekly_projections

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
    def owner_id(self) -> int:
        return self.__owner_id

    def __str__(self) -> str:
        return '%s %s (%s)' % (self.position, self.name, self.team)

    def __repr__(self) -> str:
        return self.__str__()
