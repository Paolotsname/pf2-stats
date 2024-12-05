from dataclasses import dataclass

_list = {"a": [0, 1], "b": [2, 3]}


@dataclass
class Player:
    name: str
    level: int
    armorBonus: int = 0
    saveBonus: int = 0

    def __post_init__(self):
        self.ac = _list[name][level] + armorBonus
        self.fort = _list[name][level] + saveBonus
        self.refl = _list[name][level] + saveBonus
        self.will = _list[name][level] + saveBonus


@dataclass
class Enemy:
    level: int
    armorBonus: int = 0
    saveBonus: int = 0

    def __post_init__(self):
        self.ac = _list[name][level] + armorBonus
        self.fort = _list[name][level] + saveBonus
        self.refl = _list[name][level] + saveBonus
        self.will = _list[name][level] + saveBonus
