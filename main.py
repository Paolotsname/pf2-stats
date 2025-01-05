from dataclasses import dataclass
import json

classes_dict_list = {}
with open("data.json", "r", encoding="utf-8") as f:
    classes_dict_list = json.load(f)
enemyDB = {}
with open("results.json", "r", encoding="utf-8") as f:
    enemyDB = json.load(f)


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
        enemy,
    ):

        weapon_rates0, weapon_rates1, weapon_rates2 = get_strike_rates(
            self.weaponRoll, enemy["ac"], self.weapon["agile"]
        )

        spell_ac_rates = get_d20_rates(self.spell, enemy["ac"])

        spell_fort_save_rates = get_d20_rates(enemy["fort"], self.spell + 10)
        spell_ref_save_rates = get_d20_rates(enemy["refl"], self.spell + 10)
        spell_will_save_rates = get_d20_rates(enemy["will"], self.spell + 10)

        return {
            "attacking rates": {
                "weapon_rates0": weapon_rates0,
                "weapon_rates1": weapon_rates1,
                "weapon_rates2": weapon_rates2,
                "spell_ac_rates": spell_ac_rates,
            },
            "enemy rates": {
                "spell_fort_save_rates": spell_fort_save_rates,
                "spell_ref_save_rates": spell_ref_save_rates,
                "spell_will_save_rates": spell_will_save_rates,
            },
        }

    def print_rates(self, e):
        attack_rates = self.get_rates(e)["attacking rates"]
        enemy_rates = self.get_rates(e)["enemy rates"]
        for key, value in attack_rates.items():
            print(
                f"{key}: "
                f"chance character crit fail: {value[0]}% "
                f"chance character fail chance: {value[1]}% "
                f"chance character hit chance: {value[2]}% "
                f"chance character crit hit chance: {value[3]}%"
            )
        for key, value in enemy_rates.items():
            print(
                f"{key}: "
                f"chance enemy crit fail: {value[0]}% "
                f"chance enemy fail chance: {value[1]}% "
                f"chance enemy hit chance: {value[2]}% "
                f"chance enemy crit hit chance: {value[3]}%"
            )


def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n


# a minToHit value of 11.2 means that when the dice rolls 11
# there's a 20% value of it being a failure
# and 80% value of it being a hit
# so it would be a total of 59% chance to hit before subtracting critical hits
def get_d20_rates(prof: float, ac: float) -> (float, float, float, float):
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

    # Nat 1
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

    # Nat 20
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
        round(sidesThatCritFail * 5, 2),
        round(sidesThatFail * 5, 2),
        round(sidesThatHit * 5, 2),
        round(sidesThatCritHit * 5, 2),
    )


def get_save_rates(prof, ac, profLevel):
    cf, f, s, cs = get_d20_rates(prof, ac)
    if profLevel >= 6:
        cs = s + cs
        s = 0
        if profLevel >= 8:
            f = cf + f
            cf = 0
    return cf, f, s, cs


def get_strike_rates(prof, ac, agile=0):
    if agile:
        weapon_rates0 = get_d20_rates(prof, ac)
        weapon_rates1 = get_d20_rates(prof - 4, ac)
        weapon_rates2 = get_d20_rates(prof - 8, ac)
    else:
        weapon_rates0 = get_d20_rates(prof, ac)
        weapon_rates1 = get_d20_rates(prof - 5, ac)
        weapon_rates2 = get_d20_rates(prof - 10, ac)

    return weapon_rates0, weapon_rates1, weapon_rates2


#
# ;-;
enemyy = enemyDB[0]
enemy = {}
enemy["ac"] = enemyy["avg_ac"]
enemy["fort"] = enemyy["avg_fort"]
enemy["refl"] = enemyy["avg_refl"]
enemy["will"] = enemyy["avg_will"]
test = Sheet("alchemist", 1).print_rates(enemy)
