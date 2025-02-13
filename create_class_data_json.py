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
    "Animist": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(10, 10),
        "fort": prof_list(0, 2, 18),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 12, 8),
    },
    "Alchemist": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(6, 14),
    },
    "Barbarian": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(6, 6, 8),
        "refl": prof_list(8, 12),
        "will": prof_list(14, 6),
    },
    "Bard": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(2, 18),
        "will": prof_list(0, 8, 8, 4),
    },
    "Champion": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(6, 6, 4, 4),
        "fort": prof_list(0, 8, 12),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 10, 10),
    },
    "Cleric (cloistered)": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(2, 18),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 8, 12),
    },
    "Cleric (warpriest)": {
        "weapon": prof_list(6, 12, 2),
        "spellcasting": prof_list(10, 8, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(10, 10),
        "will": prof_list(8, 12),
    },
    "Cleric (battle harbinger)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(10, 10),
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 12, 8),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 14, 6),
    },
    "Commander (playtest)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 6, 4),
        "fort": prof_list(8, 12),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(0, 10, 10),
    },
    "Druid": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(2, 18),
        "refl": prof_list(4, 16),
        "will": prof_list(10, 10),
    },
    "Exemplar": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 6, 6, 8),
    },
    "Fighter": {
        "weapon": prof_list(0, 4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 6, 4),
        "fort": prof_list(0, 8, 12),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(2, 18),
    },
    "Guardian (playtest)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(4, 6, 4, 6),
        "fort": prof_list(0, 8, 12),
        "refl": prof_list(4, 14, 2),
        "will": prof_list(0, 14, 6),
    },
    "Gunslinger": {
        "weapon": prof_list(0, 4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 16, 4),
        "refl": prof_list(0, 10, 10),
        "will": prof_list(2, 18),
    },
    "Inventor": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 16, 4),
        "refl": prof_list(6, 14),
        "will": prof_list(0, 10, 10),
    },
    "Investigator": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(8, 12),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(0, 10, 6, 4),
    },
    "Kineticist": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 6, 8, 6),
        "refl": prof_list(0, 10, 10),
        "will": prof_list(2, 18),
    },
    "Magus": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(10, 6, 4),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 8, 12),
    },
    "Monk": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(0, 12, 4, 4),
        "fort": prof_list(0, 20),
        "refl": prof_list(0, 20),
        "will": prof_list(0, 20),
    },
    "Necromancer (playtest)": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(10, 6, 4),
        "refl": prof_list(4, 16),
        "will": prof_list(2, 18),
    },
    "Oracle": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(12, 8),
        "will": prof_list(6, 10, 4),
    },
    "Psychic": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 10, 6, 4),
    },
    "Ranger": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(0, 6, 8, 6),
        "will": prof_list(2, 18),
    },
    "Rogue": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(8, 12),
        "refl": prof_list(0, 6, 6, 8),
        "will": prof_list(0, 16, 4),
    },
    "Runesmith (playtest)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(6, 14),
        "will": prof_list(0, 20),
    },
    "Sorcerer": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(4, 16),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 16, 4),
    },
    "Summoner": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(12, 8),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 14, 6),
    },
    "Swashbuckler": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(2, 18),
        "refl": prof_list(0, 6, 6, 9),
        "will": prof_list(0, 16, 4),
    },
    "Thaumaturge": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(14, 6),
        "refl": prof_list(2, 18),
        "will": prof_list(0, 6, 6, 8),
    },
    "Witch": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(4, 16),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 16, 4),
    },
    "Wizard": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 16, 4),
    },
}

save_to_file(list_classes, "class_data.json")
