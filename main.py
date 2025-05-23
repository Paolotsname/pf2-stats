from dataclasses import dataclass, field
import json
from enum import Enum

class Proficiency(Enum):
    WEAPON_ROLL = 0
    SPELL = 1
    AC = 2
    FORTITUDE = 3
    REFLEX = 4
    WILL = 5

with open("class_data.json", "r", encoding="utf-8") as f1:
    # classes_profs_json has proficiencies in this order:
    # weapon, spellcasting, armor, fortitude, reflex, will
    classes_profs_json = json.load(f1)

with open("enemy_data.json", "r", encoding="utf-8") as f2:
    enemies_stats_json = json.load(f2)


@dataclass
class Sheet:
    class_name: str
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
    vantage: str = "none"

    def __post_init__(self):
        self.profs = classes_profs_json[self.class_name]["proficiencies"][
            self.level - 1
        ]
        if self.proficiencyWithoutLevel:
            self.levelBonus = 0
        else:
            self.levelBonus = self.level
        self.weaponRoll = (
            self.profs[Proficiency.WEAPON_ROLL.value]
            + self.attributes[self.attackModifier]
            + self.weapon["bonus"]
            + self.levelBonus
        )
        self.spell = (
            self.profs[Proficiency.SPELL.value]
            + self.attributes[self.spellcastingModifier]
            + (self.levelBonus if self.profs[1] else 0)
        )
        self.ac = (
            self.profs[Proficiency.AC.value]
            + self.attributes["dex"]
            + self.armor["ACbonus"]
            + self.levelBonus
        )
        self.fort = (
            self.profs[Proficiency.FORTITUDE.value]
            + self.attributes["con"]
            + self.armor["SaveBonus"]
            + self.levelBonus
        )
        self.reflex = (
            self.profs[Proficiency.REFLEX.value]
            + self.attributes["dex"]
            + self.armor["SaveBonus"]
            + self.levelBonus
        )
        self.will = (
            self.profs[Proficiency.WILL.value]
            + self.attributes["wis"]
            + self.armor["SaveBonus"]
            + self.levelBonus
        )

        helper = classes_profs_json[self.class_name]["saveSpecialization"]
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
            self.weaponRoll,
            enemy["ac"],
            agile=self.weapon["agile"],
            vantage=self.vantage,
        )
        spell_that_target_ac_rates = get_d20_rates(self.spell, enemy["ac"])
        save_against_spell_that_target_fort = get_save_rates(
            self.fort, enemy["spell_dc"], self.saveSpecialization["fort"], self.vantage
        )
        save_against_spell_that_target_reflex = get_save_rates(
            self.reflex,
            enemy["spell_dc"],
            self.saveSpecialization["reflex"],
            self.vantage,
        )
        save_against_spell_that_target_will = get_save_rates(
            self.will, enemy["spell_dc"], self.saveSpecialization["will"], self.vantage
        )

        struck_rates = get_d20_rates(enemy["attack_bonus"], self.ac)
        spell_striked_rates = get_d20_rates(enemy["spell_attack_bonus"], self.ac)
        spell_that_target_fort_save_rates = get_d20_rates(
            enemy["fort"], self.spell + 10
        )
        spell_that_target_reflex_save_rates = get_d20_rates(
            enemy["reflex"], self.spell + 10
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
                "struck_rates": struck_rates,
                "spell_struck_rates": spell_striked_rates,
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
                f"chance character succeeds: {value[2]}% "
                f"chance character crit succeeds: {value[3]}%"
                f"  {sum(value)}"
            )
        for key, value in enemy_rates.items():
            print(
                f"{key}: "
                f"chance enemy crit fails: {value[0]}% "
                f"chance enemy fails: {value[1]}% "
                f"chance enemy succeeds: {value[2]}% "
                f"chance enemy crit succeeds: {value[3]}%"
                f"  {sum(value)}"
            )


def clamp(min_value, n, max_value) -> float:
    if n < min_value:
        return min_value
    elif n > max_value:
        return max_value
    else:
        return n


# a target of 11.2 will have the same result as the weighted average of target = 11 and target = 12,
# where target 11 has a weight of 80% and 12 has a weight of 20%
def get_d20_rates(
    proficiency: int, target: float, vantage: str = "normal"
) -> tuple[float, float, float, float]:
    if proficiency is None or target is None:
        return 0, 0, 0, 0

    # [2, 19]
    dice_faces_used = 0

    # we calculate the minimum number on dice needed for
    # (proficiency bonus + dice rolled) to be for a crit
    min_to_crit = (target + 10) - proficiency
    # we find how many faces on the dice up to 19 are crit hits
    # by subtracting the total of faces (19) by the amount that's
    # not crit hits
    ## this does mean that we are calculating the range from 19 to 1,
    ## but since we are clamping it down later,
    ## it will transform into a range from 19 to 2
    sides_that_crit_hit = 19 - (min_to_crit - 1)
    # sides_that_crit_hit can't be less than 0
    # sides_that_crit_hit can't more than 18 (number of faces between 2 and 19)
    sides_that_crit_hit = clamp(0, sides_that_crit_hit, 18)
    # we save how many faces are crit hits, so when we find how many are at least normal hits
    # we can reduce the amount that are crit hits from it and find how many are normal hits
    dice_faces_used += sides_that_crit_hit

    # then we repeat the logic for hits and fails, subtracting the sides that
    # already being accounted for for being enough for a better result

    min_to_hit = target - proficiency
    sides_that_hit = 19 - (min_to_hit - 1) - dice_faces_used
    sides_that_hit = clamp(0, sides_that_hit, 18 - dice_faces_used)
    dice_faces_used += sides_that_hit

    min_to_fail = (target - 9) - proficiency
    sides_that_fail = 19 - (min_to_fail - 1) - dice_faces_used
    sides_that_fail = clamp(0, sides_that_fail, 18 - dice_faces_used)
    dice_faces_used += sides_that_fail

    # sides_that_crit_fail will be the leftover faces
    sides_that_crit_fail = 18 - dice_faces_used

    # Nat 20 logic
    nat20_value = proficiency + 20
    # for when Nat 20 would had been at least a hit
    if nat20_value > target - 1:
        percentage_that_crit_hit = nat20_value - (target - 1)
        percentage_that_crit_hit = clamp(0, percentage_that_crit_hit, 1)
        sides_that_crit_hit += percentage_that_crit_hit
        sides_that_hit += 1 - percentage_that_crit_hit
    # for when Nat 20 would had been at least a failure
    elif nat20_value > (target - 1) - 9:
        percentage_that_hit = nat20_value - (target - 1) + 9
        percentage_that_hit = clamp(0, percentage_that_hit, 1)
        sides_that_hit += percentage_that_hit
        sides_that_fail += 1 - percentage_that_hit
    else:
        sides_that_fail += 1

    # Nat 1 logic
    nat1_value = proficiency + 1
    if nat1_value > (target - 1) + 10:
        percentage_that_hit = nat1_value - (target - 1) - 9
        percentage_that_hit = clamp(0, percentage_that_hit, 1)
        sides_that_crit_hit += percentage_that_hit
        sides_that_hit += 1 - percentage_that_hit
    # for when Nat 20 would had been at least a failure
    elif nat1_value > (target - 1):
        percentage_that_fail = nat1_value - (target - 1)
        percentage_that_fail = clamp(0, percentage_that_fail, 1)
        sides_that_fail += percentage_that_fail
        sides_that_crit_fail += 1 - percentage_that_fail
    else:
        sides_that_crit_fail += 1

    if vantage == "advantage":
        sides_that_crit_fail, sides_that_fail, sides_that_hit, sides_that_crit_hit = (
            advantagize(
                [
                    sides_that_crit_fail / 20,
                    sides_that_fail / 20,
                    sides_that_hit / 20,
                    sides_that_crit_hit / 20,
                ]
            )
        )
        return (
            round(sides_that_crit_fail * 100, 2),
            round(sides_that_fail * 100, 2),
            round(sides_that_hit * 100, 2),
            round(sides_that_crit_hit * 100, 2),
        )
    if vantage == "disadvantage":
        sides_that_crit_fail, sides_that_fail, sides_that_hit, sides_that_crit_hit = (
            disadvantagize(
                [
                    sides_that_crit_fail / 20,
                    sides_that_fail / 20,
                    sides_that_hit / 20,
                    sides_that_crit_hit / 20,
                ]
            )
        )
        return (
            round(sides_that_crit_fail * 100, 2),
            round(sides_that_fail * 100, 2),
            round(sides_that_hit * 100, 2),
            round(sides_that_crit_hit * 100, 2),
        )

    return (
        round(sides_that_crit_fail * 5, 2),
        round(sides_that_fail * 5, 2),
        round(sides_that_hit * 5, 2),
        round(sides_that_crit_hit * 5, 2),
    )


def get_save_rates(
    prof: int, target: int, prof_level: int, vantage: str = "normal"
) -> tuple[float, float, float, float]:
    cf, f, s, cs = get_d20_rates(prof, target, vantage)
    if prof_level >= 1:
        cs = s + cs
        s = 0
        if prof_level >= 2:
            f = cf + f
            cf = 0
    return cf, f, s, cs


def get_strike_rates(prof: int, target: int, vantage: str, agile: int = 0) -> tuple[
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
]:
    weapon_rates0 = get_d20_rates(prof, target, vantage)
    weapon_rates1 = get_d20_rates(prof - 5 + agile, target, vantage)
    weapon_rates2 = get_d20_rates(prof - 10 + (agile * 2), target, vantage)
    return weapon_rates0, weapon_rates1, weapon_rates2


def advantagize(a):
    answer = [0, 0, 0, 0]
    for i, result_1 in enumerate(a):
        for j, result_2 in enumerate(a):
            # index 0 will be cf, index 1 f...
            answer[max(i, j)] += result_1 * result_2
    return [round(a, 5) for a in answer]


def disadvantagize(a):
    answer = [0, 0, 0, 0]
    for i, result_1 in enumerate(a):
        for j, result_2 in enumerate(a):
            answer[min(i, j)] += result_1 * result_2
    return [round(a, 5) for a in answer]


# attackModifier = "str"
# spellcastingModifier = "cha"
# proficiencyWithoutLevel = False

enemy_level = 10
enemy_stats = enemies_stats_json[str(enemy_level)]["mean"]

Sheet(
    class_name="Fighter",
    level=10,
    attributes={"str": 4, "dex": 2, "con": 2, "int": 0, "wis": 1, "cha": 0},
    weapon={"agile": 0, "bonus": 0, "dieSize": 2},
    armor={"ACbonus": 3, "SaveBonus": 0, "cap": 0},
    vantage="none",
).print_rates(enemy_stats)

# for i in range(1, 21):
#     v = 30
#     print(i + 1 - v, get_d20_rates(i, v), i + 20 - v)
