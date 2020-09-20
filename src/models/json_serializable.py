import json
from abc import ABC, abstractmethod


class JsonSerializable(ABC):
    @abstractmethod
    def _to_dict(self) -> dict:
        pass

    def serialize(self) -> str:
        return json.dumps(self._to_dict(), separators=(',', ':'))
