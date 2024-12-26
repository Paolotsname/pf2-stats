import json


def prof_list(trainedLevels=0, expertLevels=0, masterLevels=0, legendaryLevels=0):
    return tuple(
        [2] * trainedLevels
        + [4] * expertLevels
        + [6] * masterLevels
        + [8] * legendaryLevels
    )


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


# these use normal martial scaling:
# magus eidolon battle_harbinger gunslinger_adv/oth fighter_adv
WEAPON_MARTIAL = prof_list(4, 8, 8)
WEAPON_GUARDIAN = prof_list(6, 10, 4)
WEAPON_FIGHTER_GUNSLINGER = prof_list(0, 4, 8, 8)
WEAPON_FIGHTER_OTHER = prof_list(0, 12, 6, 2)
WEAPON_SPELLCASTER = prof_list(10, 10)
WEAPON_CLERIC_WARP = prof_list(6, 12, 2)
WEAPON_ALCHEMIST = prof_list(6, 8, 6)

TODO = [-1] * 20

list_classes = {
    "alchemist": {
        "weapon": WEAPON_MARTIAL,
        "spellcasting": TODO,
        "armor": TODO,
        "fort": TODO,
        "refl": TODO,
        "will": TODO,
    },
}
dict_classes_profs = {}
for class_name in list_classes:
    print(class_name)
    dict_classes_profs[class_name] = profs_per_levels(**list_classes[class_name])
print(dict_classes_profs)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(dict_classes_profs, f, ensure_ascii=False, indent=4)
