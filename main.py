from dataclasses import dataclass
import json

classes_dict_list = {}
with open("data.json", "r", encoding="utf-8") as f:
    classes_dict_list = json.load(f)
enemyDB = [{"ac": 10, "fort": 10, "refl": 10, "will": 10}]


@dataclass
class Sheet:
    name: str
    level: int
    attributes = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}
    weapon = {"agile": 0, "bonus": 0, "dieSize": 2}
    armor = {"ACbonus": 0, "SaveBonus": 0, "cap": 0}
    attackModifier: str = "str"
    spellcastingModifier: str = "cha"

    def __post_init__(self):
        self.profs = classes_dict_list[self.name][self.level]
        self.weaponRoll = (
            self.profs[0] + self.attributes[self.attackModifier] + self.weapon["bonus"]
        )
        self.spell = self.profs[1] + self.attributes[self.spellcastingModifier]
        self.ac = self.profs[2] + self.attributes["dex"] + self.armor["ACbonus"]
        self.fort = self.profs[3] + self.attributes["con"] + self.armor["SaveBonus"]
        self.refl = self.profs[4] + self.attributes["dex"] + self.armor["SaveBonus"]
        self.will = self.profs[5] + self.attributes["wis"] + self.armor["SaveBonus"]

    def get_rates(
        self,
        enemyLevel,
    ):
        enemy = enemyDB[enemyLevel - 1]

        if self.weapon["agile"]:
            weapon_rates0 = get_rates(self.weaponRoll, enemy["ac"])
            weapon_rates1 = get_rates(self.weaponRoll - 4, enemy["ac"])
            weapon_rates2 = get_rates(self.weaponRoll - 8, enemy["ac"])
        else:
            weapon_rates0 = get_rates(self.weaponRoll, enemy["ac"])
            weapon_rates1 = get_rates(self.weaponRoll - 5, enemy["ac"])
            weapon_rates2 = get_rates(self.weaponRoll - 10, enemy["ac"])

        spell_ac_rates = get_rates(self.spell, enemy["ac"])
        spell_fort_rates = get_rates(self.spell, enemy["fort"] + 10)
        spell_ref_rates = get_rates(self.spell, enemy["refl"] + 10)
        spell_will_rates = get_rates(self.spell, enemy["will"] + 10)

        return {
            "weapon_rates0": weapon_rates0,
            "weapon_rates1": weapon_rates1,
            "weapon_rates2": weapon_rates2,
            "spell_ac_rates": spell_ac_rates,
            "spell_fort_rates": spell_fort_rates,
            "spell_ref_rates": spell_ref_rates,
            "spell_will_rates": spell_will_rates,
        }

    def print_rates(self, e):
        wasd = self.get_rates(e)
        for key, value in wasd.items():
            print(
                f"{key}: "
                f"crit fail chance: {value[0]}% "
                f"fail chance: {value[1]}% "
                f"hit chance: {value[2]}% "
                f"crit hit chance: {value[3]}%"
            )


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

    return (
        sidesThatCritFail * 5,
        sidesThatFail * 5,
        sidesThatHit * 5,
        sidesThatCritHit * 5,
    )


def get_save_rates(prof, ac, profLevel):
    rates = get_rates(prof, ac)
    if profLevel >= 6:
        cf, f, s, cs = rates
        rates = cf, f, 0, s + cs
        if profLevel >= 8:
            cf, f, s, cs = rates
            rates = 0, cf + f, s, cs
    return rates


#
test = Sheet("alchemist", 1).print_rates(1)
