import json


def prof_list(trainedLevels=0, expertLevels=0, masterLevels=0, legendaryLevels=0):
    return tuple(
        [2] * trainedLevels
        + [4] * expertLevels
        + [6] * masterLevels
        + [8] * legendaryLevels
    )


NON_CASTER = [0] * 20
TODO = [-1] * 20


def profs_per_levels(weapon, spellcasting, armor, fort, refl, will):
    _list = []
    for x in range(20):
        _list.append(
            tuple(
                [
                    weapon[x],
                    spellcasting[x],
                    armor[x],
                    fort[x],
                    refl[x],
                    will[x],
                ]
            )
        )
    return _list


def save_to_file(dict_of_lists, fileName):
    dict_classes_profs = {}
    for class_name, class_profs in dict_of_lists.items():
        dict_classes_profs[class_name] = tuple(profs_per_levels(**class_profs))
    with open(fileName, "w", encoding="utf-8") as f:
        json.dump(dict_classes_profs, f, ensure_ascii=False, indent=4)


list_classes = {
    "alchemist": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": TODO,
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(6, 14),
    },
    "barbarian": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "bard": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(2, 18),
        "will": prof_list(0, 8, 8, 4),
    },
    "champion": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "cleric (cloistered)": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "druid": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "fighter": {
        "weapon": prof_list(0, 4, 8, 8),
        "spellcasting": TODO,
        "armor": prof_list(10, 6, 4),
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "gunslinger": {
        "weapon": prof_list(0, 4, 8, 8),
        "spellcasting": TODO,
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "inventor": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": TODO,
        "armor": prof_list(10, 8, 2),
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "investigator": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "kineticist": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": TODO,
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "magus": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(10, 6, 4),
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "monk": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "oracle": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "psychic": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "ranger": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "rogue": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "sorcerer": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": TODO,
        "refl": TODO,
        "will": prof_list(0, 16, 4),
    },
    "summoner": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "swashbuckler": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "thaumaturge": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": TODO,
        "armor": prof_list(10, 8, 2),
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
    "witch": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": TODO,
        "refl": TODO,
        "will": prof_list(0, 16, 4),
    },
    "wizard": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": TODO,
        "refl": TODO,
        "will": prof_list(0, 16, 4),
    },
}

save_to_file(list_classes, "data.json")
