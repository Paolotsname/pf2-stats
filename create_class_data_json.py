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


def profs_per_levels(weapon, spellcasting, armor, fort, refl, will, saveSpecialization=None):
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
    return _list, saveSpecialization  # Return both proficiencies and saveSpecialization


def save_to_file(dict_of_lists, fileName):
    dict_classes_profs = {}
    with open(fileName, "w", encoding="utf-8") as f:
        for class_name, class_profs in dict_of_lists.items():
            # Extract saveSpecialization from the class data
            saveSpecialization = class_profs.pop("saveSpecialization", None)
            # Generate proficiencies and include saveSpecialization
            proficiencies, save_spec = profs_per_levels(saveSpecialization=saveSpecialization, **class_profs)
            # Store both in the final dictionary
            dict_classes_profs[class_name] = {
                "proficiencies": tuple(proficiencies),
                "saveSpecialization": save_spec
            }
        json.dump(dict_classes_profs, f, ensure_ascii=False, indent=4)


list_classes = {
    "Animist": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(10, 10),
        "fort": prof_list(2, 18),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 12, 8),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (13, 21),
        },
    },
    "Alchemist": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(6, 14),
        "saveSpecialization": {
            "fort": (11, 21),
            "refl": (15, 21),
            "will": (21, 21),
        },
    },
    "Barbarian": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 6, 6, 8),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 14, 6),
        "saveSpecialization": {
            "fort": (7, 13),
            "refl": (21, 21),
            "will": (15, 21),
        },
    },
    "Bard": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(2, 18),
        "will": prof_list(0, 8, 8, 4),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (9, 17),
        },
    },
    "Champion": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(6, 6, 4, 4),
        "fort": prof_list(0, 8, 12),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 10, 10),
        "saveSpecialization": {
            "fort": (9, 21),
            "refl": (21, 21),
            "will": (11, 21),
        },
    },
    "Cleric (cloistered)": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(2, 18),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 8, 12),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (9, 21),
        },
    },
    "Cleric (warpriest)": {
        "weapon": prof_list(6, 12, 2),
        "spellcasting": prof_list(10, 8, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 8, 12),
        "saveSpecialization": {
            "fort": (15, 21),
            "refl": (21, 21),
            "will": (9, 21),
        },
    },
    "Cleric (battle harbinger)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(10, 10),
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 12, 8),
        "refl": prof_list(10, 10),
        "will": prof_list(0, 14, 6),
        "saveSpecialization": {
            "fort": (13, 21),
            "refl": (21, 21),
            "will": (21, 21),
        },
    },
    "Commander (playtest)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 6, 4),
        "fort": prof_list(8, 12),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(0, 10, 10),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (15, 21),
            "will": (11, 21),
        },
    },
    "Druid": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(2, 18),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 10, 10),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (11, 21),
        },
    },
    "Exemplar": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 6, 6, 8),
        "saveSpecialization": {
            "fort": (15, 21),
            "refl": (21, 21),
            "will": (7, 13),
        },
    },
    "Fighter": {
        "weapon": prof_list(0, 4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 6, 4),
        "fort": prof_list(0, 8, 12),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(2, 18),
        "saveSpecialization": {
            "fort": (9, 21),
            "refl": (15, 21),
            "will": (21, 21),
        },
    },
    "Guardian (playtest)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(4, 6, 4, 6),
        "fort": prof_list(0, 8, 12),
        "refl": prof_list(4, 14, 2),
        "will": prof_list(0, 14, 6),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (19, 21),
            "will": (15, 21),
        },
    },
    "Gunslinger": {
        "weapon": prof_list(0, 4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 16, 4),
        "refl": prof_list(0, 10, 10),
        "will": prof_list(2, 18),
        "saveSpecialization": {
            "fort": (17, 21),
            "refl": (11, 21),
            "will": (21, 21),
        },
    },
    "Inventor": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 16, 4),
        "refl": prof_list(6, 14),
        "will": prof_list(0, 10, 10),
        "saveSpecialization": {
            "fort": (17, 21),
            "refl": (21, 21),
            "will": (11, 21),
        },
    },
    "Investigator": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(8, 12),
        "refl": prof_list(0, 14, 6),
        "will": prof_list(0, 10, 6, 4),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (15, 21),
            "will": (11, 17),
        },
    },
    "Kineticist": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 6, 8, 6),
        "refl": prof_list(0, 10, 10),
        "will": prof_list(2, 18),
        "saveSpecialization": {
            "fort": (7, 15),
            "refl": (11, 21),
            "will": (21, 21),
        },
    },
    "Magus": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(10, 6, 4),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 8, 12),
        "saveSpecialization": {
            "fort": (15, 21),
            "refl": (21, 21),
            "will": (9, 21),
        },
    },
    "Monk": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(0, 12, 4, 4),
        "fort": prof_list(0, 20),
        "refl": prof_list(0, 20),
        "will": prof_list(0, 20),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (21, 21),
        },
    },
    "Necromancer (playtest)": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(0, 10, 6, 4),
        "refl": prof_list(4, 16),
        "will": prof_list(2, 18),
        "saveSpecialization": {
            "fort": (11, 17),
            "refl": (21, 21),
            "will": (21, 21),
        },
    },
    "Oracle": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(12, 8),
        "will": prof_list(0, 6, 10, 4),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (7, 17),
        },
    },
    "Psychic": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 10, 6, 4),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (11, 17),
        },
    },
    "Ranger": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(0, 6, 8, 6),
        "will": prof_list(2, 18),
        "saveSpecialization": {
            "fort": (11, 21),
            "refl": (7, 15),
            "will": (21, 21),
        },
    },
    "Rogue": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(8, 12),
        "refl": prof_list(0, 6, 6, 8),
        "will": prof_list(0, 16, 4),
        "saveSpecialization": {
            "fort": (9, 21),
            "refl": (7, 13),
            "will": (17, 21),
        },
    },
    "Runesmith (playtest)": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(6, 14),
        "will": prof_list(0, 20),
        "saveSpecialization": {
            "fort": (11, 21),
            "refl": (21, 21),
            "will": (21, 21),
        },
    },
    "Sorcerer": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(4, 16),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 16, 4),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (17, 21),
        },
    },
    "Summoner": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": prof_list(8, 8, 4),
        "armor": prof_list(12, 8),
        "fort": prof_list(0, 10, 10),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 14, 6),
        "saveSpecialization": {
            "fort": (11, 21),
            "refl": (21, 21),
            "will": (15, 21),
        },
    },
    "Swashbuckler": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(12, 6, 2),
        "fort": prof_list(2, 18),
        "refl": prof_list(0, 6, 6, 9),
        "will": prof_list(0, 16, 4),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (7, 13),
            "will": (17, 21),
        },
    },
    "Thaumaturge": {
        "weapon": prof_list(4, 8, 8),
        "spellcasting": NON_CASTER,
        "armor": prof_list(10, 8, 2),
        "fort": prof_list(0, 14, 6),
        "refl": prof_list(2, 18),
        "will": prof_list(0, 6, 6, 8),
        "saveSpecialization": {
            "fort": (15, 21),
            "refl": (21, 21),
            "will": (7, 13),
        },
    },
    "Witch": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(4, 16),
        "refl": prof_list(8, 12),
        "will": prof_list(0, 16, 4),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (17, 21),
        },
    },
    "Wizard": {
        "weapon": prof_list(10, 10),
        "spellcasting": prof_list(6, 8, 4, 2),
        "armor": prof_list(12, 8),
        "fort": prof_list(8, 12),
        "refl": prof_list(4, 16),
        "will": prof_list(0, 16, 4),
        "saveSpecialization": {
            "fort": (21, 21),
            "refl": (21, 21),
            "will": (17, 21),
        },
    },
}

save_to_file(list_classes, "class_data.json")
