from dataclasses import dataclass
import json

classes_profs_json = {}
with open("data.json", "r", encoding="utf-8") as f:
    classes_profs_json = json.load(f)
enemy_avg_json = {}
with open("results.json", "r", encoding="utf-8") as f:
    enemy_avg_json = json.load(f)


@dataclass
class Sheet:
    name: str
    level: int
    attributes = {"str": 0, "dex": 0, "con": 0, "int": 0, "wis": 0, "cha": 0}
    weapon = {"agile": 0, "bonus": 0, "dieSize": 2}
    armor = {"ACbonus": 0, "SaveBonus": 0, "cap": 0}
    attackModifier: str = "str"
    spellcastingModifier: str = "cha"
    proficiencyWithoutLevel: bool = False

    def __post_init__(self):
        # profs are, in order: weapon, spellcasting ,armor ,fortitude, reflex, will
        self.profs = classes_profs_json[self.name][self.level]
        if self.proficiencyWithoutLevel:
            self.proficiencyBonus = 0
        else:
            self.proficiencyBonus = self.level
        self.weaponRoll = (
            self.profs[0]
            + self.attributes[self.attackModifier]
            + self.weapon["bonus"]
            + self.proficiencyBonus
        )
        self.spell = (
            self.profs[1]
            + self.attributes[self.spellcastingModifier]
            + self.proficiencyBonus
        )
        self.ac = (
            self.profs[2]
            + self.attributes["dex"]
            + self.armor["ACbonus"]
            + self.proficiencyBonus
        )
        self.fort = (
            self.profs[3]
            + self.attributes["con"]
            + self.armor["SaveBonus"]
            + self.proficiencyBonus
        )
        self.reflex = (
            self.profs[4]
            + self.attributes["dex"]
            + self.armor["SaveBonus"]
            + self.proficiencyBonus
        )
        self.will = (
            self.profs[5]
            + self.attributes["wis"]
            + self.armor["SaveBonus"]
            + self.proficiencyBonus
        )

    def get_rates(
        self,
        enemy,
    ):

        weapon_map0, weapon_map1, weapon_map2 = get_strike_rates(
            self.weaponRoll, enemy["ac"], self.weapon["agile"]
        )
        spell_that_target_ac_rates = get_d20_rates(self.spell, enemy["ac"])
        save_against_spell_that_target_fort = get_d20_rates(
            self.fort, enemy["spell_dc"]
        )
        save_against_spell_that_target_reflex = get_d20_rates(
            self.reflex, enemy["spell_dc"]
        )
        save_against_spell_that_target_will = get_d20_rates(
            self.fort, enemy["spell_dc"]
        )

        striked_rates = get_d20_rates(enemy["attack_bonus"], self.ac)
        spell_striked_rates = get_d20_rates(enemy["spell_attack_bonus"], self.ac)
        spell_that_target_fort_save_rates = get_d20_rates(
            enemy["fort"], self.spell + 10
        )
        spell_that_target_reflex_save_rates = get_d20_rates(
            enemy["refl"], self.spell + 10
        )
        spell_that_target_will_save_rates = get_d20_rates(
            enemy["will"], self.spell + 10
        )

        return {
            "player_rolls_rates": {
                "weapon_map0": weapon_map0,
                "weapon_map1": weapon_map1,
                "weapon_map2": weapon_map2,
                "spell_that_target_ac_rates": spell_that_target_ac_rates,
                "save_against_spell_that_target_fort": save_against_spell_that_target_fort,
                "save_against_spell_that_target_reflex": save_against_spell_that_target_reflex,
                "save_against_spell_that_target_will": save_against_spell_that_target_will,
            },
            "enemy_rolls_rates": {
                "striked_rates": striked_rates,
                "spell_striked_rates": spell_striked_rates,
                "spell_that_target_fort_save_rates": spell_that_target_fort_save_rates,
                "spell_that_target_reflex_save_rates": spell_that_target_reflex_save_rates,
                "spell_that_target_will_save_rates": spell_that_target_will_save_rates,
            },
        }

    def print_rates(self, enemy):
        rates = self.get_rates(enemy)
        attack_rates = rates["player_rolls_rates"]
        enemy_rates = rates["enemy_rolls_rates"]
        for key, value in attack_rates.items():
            print(
                f"{key}: "
                f"chance character crit fails: {value[0]}% "
                f"chance character fails: {value[1]}% "
                f"chance character hits: {value[2]}% "
                f"chance character crit hits: {value[3]}%"
            )
        for key, value in enemy_rates.items():
            print(
                f"{key}: "
                f"chance enemy crit fails: {value[0]}% "
                f"chance enemy fails: {value[1]}% "
                f"chance enemy hits: {value[2]}% "
                f"chance enemy crit hits: {value[3]}%"
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
def get_d20_rates(proficiency: int, target: float) -> (float, float, float, float):
    if proficiency is None or target is None:
        print("enemy has null value")
        return (0, 0, 0, 0)

    # 2-19
    diceFacesUsed = 0

    # defender's critical ac minus attacker's modifier and a +1 to create an offset and start at a dice value 2
    minToCrit = (target + 10) - proficiency + 1
    sidesThatCritHit = clamp(21 - minToCrit, 0, 18 - diceFacesUsed)
    diceFacesUsed += sidesThatCritHit

    minToHit = (target) - proficiency + 1
    sidesThatHit = clamp(21 - minToHit - diceFacesUsed, 0, 18 - diceFacesUsed)
    diceFacesUsed += sidesThatHit

    minToFail = (target - 9) - proficiency + 1
    sidesThatFail = clamp(21 - minToFail - diceFacesUsed, 0, 18 - diceFacesUsed)
    diceFacesUsed += sidesThatFail

    sidesThatCritFail = 18 - diceFacesUsed

    # Nat 1
    Nat1Value = proficiency + 1
    if Nat1Value >= target + 10:
        value = clamp(Nat1Value - target + 10 + 1, 0, 1)
        sidesThatHit += value
        sidesThatFail += 1 - value
    elif Nat1Value >= target:
        value = clamp(Nat1Value - target + 1, 0, 1)
        sidesThatFail += value
        sidesThatCritFail += 1 - value
    else:
        sidesThatCritFail += 1

    # Nat 20
    Nat20Value = proficiency + 20
    if Nat20Value + 1 >= target:
        value = clamp(Nat20Value - target + 1, 0, 1)
        sidesThatCritHit += value
        sidesThatHit += 1 - value
    elif Nat20Value + 1 > target - 10:
        value = clamp(Nat20Value - target + 10, 0, 1)
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


def get_save_rates(prof, target, profLevel):
    cf, f, s, cs = get_d20_rates(prof, target)
    if profLevel >= 6:
        cs = s + cs
        s = 0
        if profLevel >= 8:
            f = cf + f
            cf = 0
    return cf, f, s, cs


def get_strike_rates(prof, target, agile=0):
    if agile:
        weapon_rates0 = get_d20_rates(prof, target)
        weapon_rates1 = get_d20_rates(prof - 4, target)
        weapon_rates2 = get_d20_rates(prof - 8, target)
    else:
        weapon_rates0 = get_d20_rates(prof, target)
        weapon_rates1 = get_d20_rates(prof - 5, target)
        weapon_rates2 = get_d20_rates(prof - 10, target)

    return weapon_rates0, weapon_rates1, weapon_rates2


#
# c:
enemy_level = 1
enemy = enemy_avg_json[enemy_level + 1]["avg"]
test = Sheet("alchemist", 1).print_rates(enemy)
