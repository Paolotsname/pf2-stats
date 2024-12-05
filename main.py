from enum import auto, Enum
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


def all_get_rates(
    playerclass, level, attributes, bonuses, flags={"agile": False, "finesse": False}
):
    player = playerclass.getProficiencies(level)
    enemy = enemyModes[level - 1]

    if flags["agile"]:
        if flags["finesse"]:
            weapon_rates0 = get_rates(player.weapon + attributes["str"], enemy.ac)
            weapon_rates1 = get_rates(player.weapon - 4 + attributes["str"], enemy.ac)
            weapon_rates2 = get_rates(player.weapon - 8 + attributes["str"], enemy.ac)
        else:
            weapon_rates0 = get_rates(player.weapon + attributes["dex"], enemy.ac)
            weapon_rates1 = get_rates(player.weapon - 5 + attributes["dex"], enemy.ac)
            weapon_rates2 = get_rates(player.weapon - 10 + attributes["dex"], enemy.ac)

    spell_ac_rates = get_rates(player.spell + attributes[scm], enemy.ac)
    spell_fort_rates = get_rates(player.spell + attributes[scm], enemy.fort + 10)
    spell_ref_rates = get_rates(player.spell + attributes[scm], enemy.ref + 10)
    spell_will_rates = get_rates(player.spell + attributes[scm], enemy.will + 10)

    ac_rates = get_rates(enemy.normal_attack, player.ac)
    fort_rates = get_rates(enemy.spell_attack, player.fort + 10)
    ref_rates = get_rates(enemy.spell_attack, player.ref + 10)
    will_rates = get_rates(enemy.spell_attack, player.will + 10)

    return weapon_rates, spell_rates


attributes = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}

bonuses = {"circumstance": 0, "item": 0, "status": 0}


def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n


# a minToHit value of 11.2 means that when the dice rolls 11
# there's a 20% chance of it being a failure
# and 80% chance of it being a hit
# so it would be a total of 59% chance to hit before subtracting critical hits
def get_rates(prof, ac):
    # 2-19
    diceFacesUsed = 0

    # defender's critical ac minus attacker's modifier and a +1 to create an offset and start at a dice value 2
    minToCrit = (ac + 10) - prof + 1
    sidesThatCritHit = clamp(21 - minToCrit, 0, 18 - diceFacesUsed)
    diceFacesUsed += sidesThatCritHit

    minToHit = (ac) - prof + 1
    sidesThatHit = clamp(21 - minToHit - diceFacesUsed, 0, 18 - diceFacesUsed)
    diceFacesUsed += sidesThatHit

    minToFail = (ac - 9) - prof + 1
    sidesThatFail = clamp(21 - minToFail - diceFacesUsed, 0, 18 - diceFacesUsed)
    diceFacesUsed += sidesThatFail

    sidesThatCritFail = 18 - diceFacesUsed

    Nat1Value = prof + 1
    if Nat1Value >= ac + 10:
        value = clamp(Nat1Value - ac + 10 + 1, 0, 1)
        sidesThatHit += value
        sidesThatFail += 1 - value
    elif Nat1Value >= ac:
        value = clamp(Nat1Value - ac + 1, 0, 1)
        sidesThatFail += value
        sidesThatCritFail += 1 - value
    else:
        sidesThatCritFail += 1
    # 20
    Nat20Value = prof + 20
    if Nat20Value + 1 >= ac:
        value = clamp(Nat20Value - ac + 1, 0, 1)
        sidesThatCritHit += value
        sidesThatHit += 1 - value
    elif Nat20Value + 1 > ac - 10:
        value = clamp(Nat20Value - ac + 10, 0, 1)
        sidesThatHit += value
        sidesThatFail += 1 - value
    else:
        sidesThatFail += 1

    return (sidesThatCritFail, sidesThatFail, sidesThatHit, sidesThatCritHit)


prof = 11
dc = 30.1

a, b = all_get_rates(alchemist, 1, attributes, bonuses)

print(a)
print(b)
