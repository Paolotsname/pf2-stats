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
    with open(fileName, "w", encoding="utf-8") as f:
        for class_name, class_profs in dict_of_lists.items():
            dict_classes_profs[class_name] = tuple(profs_per_levels(**class_profs))
        json.dump(dict_classes_profs, f, ensure_ascii=False, indent=4)


list_classes = {
    "animist": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(10, 10),
        "fort": prof_list(0, 2, 18),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 12, 8),
    },
    "alchemist": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(6, 14),
    },
    "barbarian": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(6, 6, 8),
        "refl": prof_list(8, 12),
        "will": prof_list(14, 6),
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
        "armor": prof_list(6, 6, 4, 4),
        "fort": prof_list(0, 8, 12),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 10, 10),
    },
    "cleric (cloistered)": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(2, 18),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 8, 12),
    },
    "cleric (warpriest)": {
        "weapon": prof_list(6, 12, 2),
        "spellcasting": prof_list(10, 8, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(10, 10),
        "will": prof_list(8, 12),
    },
    "cleric (battle harbinger)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(10, 10),
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 12, 8),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 14, 6),
    },
    "commander (playtest)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 6, 4),
        "fort": prof_list(8, 12),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(0, 10, 10),
    },
    "druid": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(2, 18),
        "refl": prof_list(4, 16),
        "will": prof_list(10, 10),
    },
    "exemplar": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 6, 6, 8),
    },
    "fighter": {
        "weapon": prof_list(0, 4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 6, 4),
        "fort": prof_list(0, 8, 12),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(2, 18),
    },
    "guardian (playtest)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(4, 6, 4, 6),
        "fort": prof_list(0, 8, 12),
        "refl": prof_list(4, 14, 2),
        "will": prof_list(0, 14, 6),
    },
    "gunslinger": {
        "weapon": prof_list(0, 4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 16, 4),
        "refl": prof_list(0, 10, 10),
        "will": prof_list(2, 18),
    },
    "inventor": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 16, 4),
        "refl": prof_list(6, 14),
        "will": prof_list(0, 10, 10),
    },
    "investigator": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(8, 12),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(0, 10, 6, 4),
    },
    "kineticist": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 6, 8, 6),
        "refl": prof_list(0, 10, 10),
        "will": prof_list(2, 18),
    },
    "magus": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(10, 6, 4),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 8, 12),
    },
    "monk": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(0, 12, 4, 4),
        "fort": prof_list(0, 20),
        "refl": prof_list(0, 20),
        "will": prof_list(0, 20),
    },
    "necromancer (playtest)": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(10, 6, 4),
        "refl": prof_list(4, 16),
        "will": prof_list(2, 18),
    },
    "oracle": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(12, 8),
        "will": prof_list(6, 10, 4),
    },
    "psychic": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 10, 6, 4),
    },
    "ranger": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(0, 6, 8, 6),
        "will": prof_list(2, 18),
    },
    "rogue": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(8, 12),
        "refl": prof_list(0, 6, 6, 8),
        "will": prof_list(0, 16, 4),
    },
    "runesmith (playtest)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(6, 14),
        "will": prof_list(0, 20),
    },
    "sorcerer": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(4, 16),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 16, 4),
    },
    "summoner": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(12, 8),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 14, 6),
    },
    "swashbuckler": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(2, 18),
        "refl": prof_list(0, 6, 6, 9),
        "will": prof_list(0, 16, 4),
    },
    "thaumaturge": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(14, 6),
        "refl": prof_list(2, 18),
        "will": prof_list(0, 6, 6, 8),
    },
    "witch": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(4, 16),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 16, 4),
    },
    "wizard": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 16, 4),
    },
}

save_to_file(list_classes, "class_data.json")
