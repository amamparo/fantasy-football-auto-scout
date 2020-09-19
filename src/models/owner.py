class Owner:
    def __init__(self, _id: int, name: str, is_active: bool, is_current_user: bool):
        self.__id = _id
        self.__name = name
        self.__is_active = is_active
        self.__is_current_user = is_current_user

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @property
    def is_current_user(self) -> bool:
        return self.__is_current_user

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()
