from typing import Dict

from src.models.json_serializable import JsonSerializable


class LeagueSettings(JsonSerializable):

    def __init__(self, num_weeks: int, starters_by_position: Dict[str, int], has_flex: bool):
        self.__num_weeks = num_weeks
        self.__starters_by_position = starters_by_position
        self.__has_flex = has_flex

    def _to_dict(self) -> dict:
        return {
            'num_weeks': self.__num_weeks,
            'starters_by_position': self.__starters_by_position,
            'has_flex': self.__has_flex
        }
