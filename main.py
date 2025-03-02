from dataclasses import dataclass, field
import json

with open("class_data.json", "r", encoding="utf-8") as f:
    # classes_profs_json has proficiencies in this order:
    # weapon, spellcasting, armor, fortitude, reflex, will
    classes_profs_json = json.load(f)

with open("enemy_data.json", "r", encoding="utf-8") as f:
    enemies_stats_json = json.load(f)


@dataclass
class Sheet:
    name: str
    level: int
    attributes: dict = field(
        default_factory=lambda: {
            "str": 0,
            "dex": 0,
            "con": 0,
            "int": 0,
            "wis": 0,
            "cha": 0,
        }
    )
    weapon: dict = field(default_factory=lambda: {"agile": 0, "bonus": 0, "dieSize": 2})
    armor: dict = field(
        default_factory=lambda: {"ACbonus": 0, "SaveBonus": 0, "cap": 0}
    )
    attackModifier: str = "str"
    spellcastingModifier: str = "cha"
    proficiencyWithoutLevel: bool = False

    def __post_init__(self):
        self.profs = classes_profs_json[self.name]["proficiencies"][self.level]
        if self.proficiencyWithoutLevel:
            self.levelBonus = 0
        else:
            self.levelBonus = self.level
        self.weaponRoll = (
            self.profs[0]
            + self.attributes[self.attackModifier]
            + self.weapon["bonus"]
            + self.levelBonus
        )
        self.spell = (
            self.profs[1] + self.attributes[self.spellcastingModifier] + self.levelBonus
        )
        self.ac = (
            self.profs[2]
            + self.attributes["dex"]
            + self.armor["ACbonus"]
            + self.levelBonus
        )
        self.fort = (
            self.profs[3]
            + self.attributes["con"]
            + self.armor["SaveBonus"]
            + self.levelBonus
        )
        self.reflex = (
            self.profs[4]
            + self.attributes["dex"]
            + self.armor["SaveBonus"]
            + self.levelBonus
        )
        self.will = (
            self.profs[5]
            + self.attributes["wis"]
            + self.armor["SaveBonus"]
            + self.levelBonus
        )

        helper = classes_profs_json[self.name]["saveSpecialization"]
        if self.level >= helper["fort"][0]:
            if self.level >= helper["fort"][1]:
                fort_level = 2
            else:
                fort_level = 1
        else:
            fort_level = 0

        if self.level >= helper["reflex"][0]:
            if self.level >= helper["reflex"][1]:
                reflex_level = 2
            else:
                reflex_level = 1
        else:
            reflex_level = 0

        if self.level >= helper["will"][0]:
            if self.level >= helper["will"][1]:
                will_level = 2
            else:
                will_level = 1
        else:
            will_level = 0
        self.saveSpecialization = {
            "fort": fort_level,
            "reflex": reflex_level,
            "will": will_level,
        }

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
        spell_that_target_fort_save_rates = get_save_rates(
            enemy["fort"], self.spell + 10, self.saveSpecialization["fort"]
        )
        spell_that_target_reflex_save_rates = get_save_rates(
            enemy["reflex"], self.spell + 10, self.saveSpecialization["reflex"]
        )
        spell_that_target_will_save_rates = get_save_rates(
            enemy["will"], self.spell + 10, self.saveSpecialization["will"]
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
                f"  {sum(value)}"
            )
        for key, value in enemy_rates.items():
            print(
                f"{key}: "
                f"chance enemy crit fails: {value[0]}% "
                f"chance enemy fails: {value[1]}% "
                f"chance enemy hits: {value[2]}% "
                f"chance enemy crit hits: {value[3]}%"
                f"  {sum(value)}"
            )


def clamp(minValue, n, maxValue) -> float:
    if n < minValue:
        return minValue
    elif n > maxValue:
        return maxValue
    else:
        return n


# a target of 11.2 is calculated by taking
# the rates for target 11 and target 12.
# then calculating them together with:
# 20% of the rates for target 11
# 80% of the rates for target 12
# so it would be a total of 59% chance to hit before subtracting critical hits
def get_d20_rates(proficiency: int, target: float) -> tuple[float, float, float, float]:
    if proficiency is None or target is None:
        print("enemy has null value")
        return (0, 0, 0, 0)

    # [2, 19]
    diceFacesUsed = 0

    # we calculate the minimum number on dice needed for
    # (proficiency bonus + dice rolled) to be for a crit
    minToCrit = (target + 10) - proficiency
    # we find how many faces on the dice up to 19 are crit hits
    # by subtracting the total of faces (19) by the amout that's
    # not crit hits
    ## this does mean that we are calculating the range from 1 to 19,
    ## but since we are clamping it down later it doesn't matter
    sidesThatCritHit = 19 - (minToCrit - 1)
    # sidesThatCritHit can't be less than 0
    # sidesThatCritHit can't more than 18 (number of faces between 2 and 19)
    sidesThatCritHit = clamp(0, sidesThatCritHit, 18)
    # we save how many faces are crit hits, so when we find how many are at least normal hits
    # we can reduce the amount that are crit hits from it and find how many are normal hits
    diceFacesUsed += sidesThatCritHit

    minToHit = (target) - proficiency
    sidesThatHit = 19 - (minToHit - 1) - diceFacesUsed
    sidesThatHit = clamp(0, sidesThatHit, 18 - diceFacesUsed)
    diceFacesUsed += sidesThatHit

    minToFail = (target - 9) - proficiency
    sidesThatFail = 19 - (minToFail - 1) - diceFacesUsed
    sidesThatFail = clamp(0, sidesThatFail, 18 - diceFacesUsed)
    diceFacesUsed += sidesThatFail

    # sidesThatCritFail will be the leftover faces
    sidesThatCritFail = 18 - diceFacesUsed

    # Nat 20
    Nat20Value = proficiency + 20
    # for when Nat 20 will be at least a hit
    if Nat20Value > target - 1:
        percentageThatCritHit = Nat20Value - (target - 1)
        percentageThatCritHit = clamp(0, percentageThatCritHit, 1)
        sidesThatCritHit += percentageThatCritHit
        sidesThatHit += 1 - percentageThatCritHit
    # for when Nat 20 will be at least a failure
    elif Nat20Value > (target - 1) - 9:
        percentageThatHit = Nat20Value - (target - 1) + 9
        percentageThatHit = clamp(0, percentageThatHit, 1)
        sidesThatHit += percentageThatHit
        sidesThatFail += 1 - percentageThatHit
    else:
        sidesThatFail += 1

    # Nat 1
    Nat1Value = proficiency + 1
    if Nat1Value > (target - 1) + 10:
        percentageThatHit = Nat1Value - (target - 1) - 9
        percentageThatHit = clamp(0, percentageThatHit, 1)
        sidesThatCritHit += percentageThatHit
        sidesThatHit += 1 - percentageThatHit
    # for when Nat 20 will be at least a failure
    elif Nat1Value > (target - 1):
        percentageThatFail = Nat1Value - (target - 1)
        percentageThatFail = clamp(0, percentageThatFail, 1)
        sidesThatFail += percentageThatFail
        sidesThatCritFail += 1 - percentageThatFail
    else:
        sidesThatCritFail += 1

    return (
        round(sidesThatCritFail * 5, 2),
        round(sidesThatFail * 5, 2),
        round(sidesThatHit * 5, 2),
        round(sidesThatCritHit * 5, 2),
    )


def get_save_rates(prof, target, profLevel) -> tuple[float, float, float, float]:
    cf, f, s, cs = get_d20_rates(prof, target)
    if profLevel >= 1:
        cs = s + cs
        s = 0
        if profLevel >= 2:
            f = cf + f
            cf = 0
    return cf, f, s, cs


def get_strike_rates(prof, target, agile=0) -> tuple[
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
]:
    weapon_rates0 = get_d20_rates(prof, target)
    weapon_rates1 = get_d20_rates(prof - 5 + agile, target)
    weapon_rates2 = get_d20_rates(prof - 10 + (agile * 2), target)
    return weapon_rates0, weapon_rates1, weapon_rates2


#
# c:
# enemy_level = 1
# enemy = enemies_stats_json[enemy_level + 1]["mean"]
# test = Sheet(
#     "Fighter",
#     1,
#     attributes={"str": 4, "dex": 2, "con": 2, "int": 0, "wis": 1, "cha": 0},
# ).print_rates(enemy)
for i in range(1, 21):
   v = 30
   print(i + 1 - v, get_d20_rates(i, v), i + 20 - v)
