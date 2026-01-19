from enum import Enum


class TestEnum(Enum):
    BELBIN = (1, "Тест Белбина", "Тест на тип команды", "/belbin_test")
    DISC = (2, "Тест DISC", "Тест на поведенческий стиль", "/disc_test")
    def __init__(self, id: int, display_name: str, description: str, url: str):
        self.id = id
        self.display_name = display_name
        self.description = description
        self.url = url
