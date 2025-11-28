import eel
import sys

from models.statics_db import RUNES, RUNEKEYS, SUMMONER, CHAMPIONS, ITEMS
import config

from asyncio import run_coroutine_threadsafe
import lcu

# Store runes for both champions
runes_champion_1 = []
runes_champion_2 = []


def close_callback(route, websockets):
    if not websockets:
        sys.exit()


eel.init("web")


def set_spells(champion_num, champion):
    eel.set_title(champion_num, "spells", "Spells")

    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_champion_img(
        champion_num,
        "champion",
        "https://ddragon.leagueoflegends.com/cdn/img/champion/loading/"
        + entry.champion
        + "_0.jpg",
    )

    eel.set_spell_img(
        champion_num,
        "img_passive",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/passive/"
        + entry.spell_image_passive,
    )
    eel.set_spell_img(
        champion_num,
        "img_Q",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/spell/"
        + entry.spell_image_q,
    )
    eel.set_spell_img(
        champion_num,
        "img_W",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/spell/"
        + entry.spell_image_w,
    )
    eel.set_spell_img(
        champion_num,
        "img_E",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/spell/"
        + entry.spell_image_e,
    )
    eel.set_spell_img(
        champion_num,
        "img_R",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/spell/"
        + entry.spell_image_r,
    )

    eel.set_spell_text(
        champion_num,
        entry.spell_text_passive,
        entry.spell_text_q,
        entry.spell_text_w,
        entry.spell_text_e,
        entry.spell_text_r,
    )

    eel.set_spell_src(
        champion_num,
        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_P1.webm".format(
            championId=champion
        ),
        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_Q1.webm".format(
            championId=champion
        ),
        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_W1.webm".format(
            championId=champion
        ),
        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_E1.webm".format(
            championId=champion
        ),
        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_R1.webm".format(
            championId=champion
        ),
    )


def set_spell_order(champion_num, champion, skills):
    dict = {
        1: CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_q,
        2: CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_w,
        3: CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_e,
        4: CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_r,
    }

    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_title(champion_num, "spell-order", "Spell-order")
    
    for i in range(1, 9):
        eel.set_spell_name(champion_num, f"skill-{i}-name", skills[i-1])
        eel.set_spell_order(
            champion_num,
            f"skill-{i}",
            "https://ddragon.leagueoflegends.com/cdn/"
            + version
            + "/img/spell/"
            + dict[skills[i-1]],
        )


def set_summs(champion_num, champion, summ):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_title(champion_num, "summoner-spells", "Summoner Spells")
    eel.set_summ(
        champion_num,
        "summ-1",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/spell/"
        + SUMMONER.get(SUMMONER.key == summ[0]).id
        + ".png",
    )
    eel.set_summ(
        champion_num,
        "summ-2",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/spell/"
        + SUMMONER.get(SUMMONER.key == summ[1]).id
        + ".png",
    )

    eel.set_summ_text(
        champion_num,
        SUMMONER.get(SUMMONER.key == summ[0]).description,
        SUMMONER.get(SUMMONER.key == summ[1]).description,
    )


def set_items(champion_num, champion, items):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_title(champion_num, "items", "Builds")
    
    item_ids = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9"]
    item_names = []
    
    for idx, item_id in enumerate(item_ids):
        row = idx // 3
        col = idx % 3
        eel.set_item(
            champion_num,
            item_id,
            "https://ddragon.leagueoflegends.com/cdn/"
            + version
            + "/img/item/"
            + ITEMS.get(ITEMS.id == items[row][col]).id
            + ".png",
        )
        item_names.append(ITEMS.get(ITEMS.id == items[row][col]).name)

    eel.set_item_text(champion_num, *item_names)


def set_start_items(champion_num, champion, items):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_title(champion_num, "start-items", "Start Items")
    for i in range(len(items[0])):
        eel.set_item(
            champion_num,
            "start-item" + str(i + 1),
            "https://ddragon.leagueoflegends.com/cdn/"
            + version
            + "/img/item/"
            + ITEMS.get(ITEMS.id == items[0][i]).id
            + ".png",
        )

    names = [(ITEMS.get(ITEMS.id == items[0][i]).name) for i in range(len(items[0]))]
    for i in range(len(items[0]), 3):
        names.append("")

    eel.set_start_item_text(champion_num, names[0], names[1], names[2])


def set_boots(champion_num, champion, items):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_title(champion_num, "boots", "Boots")
    eel.set_item(
        champion_num,
        "boots1",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/item/"
        + ITEMS.get(ITEMS.id == items[0]).id
        + ".png",
    )
    eel.set_item(
        champion_num,
        "boots2",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/item/"
        + ITEMS.get(ITEMS.id == items[1]).id
        + ".png",
    )
    eel.set_item(
        champion_num,
        "boots3",
        "https://ddragon.leagueoflegends.com/cdn/"
        + version
        + "/img/item/"
        + ITEMS.get(ITEMS.id == items[2]).id
        + ".png",
    )

    eel.set_boots_text(
        champion_num,
        ITEMS.get(ITEMS.id == items[0]).name,
        ITEMS.get(ITEMS.id == items[1]).name,
        ITEMS.get(ITEMS.id == items[2]).name,
    )


def set_core_items(champion_num, champion, items):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    for item in [0, 1054, 1055, 1056]:
        try:
            items.remove(item)
        except:
            pass

    eel.set_title(champion_num, "core-items", "Core Items")
    
    for i in range(6):
        eel.set_item(
            champion_num,
            f"core-item{i+1}",
            "https://ddragon.leagueoflegends.com/cdn/"
            + version
            + "/img/item/"
            + ITEMS.get(ITEMS.id == items[i]).id
            + ".png",
        )

    eel.set_core_item_text(
        champion_num,
        ITEMS.get(ITEMS.id == items[0]).name,
        ITEMS.get(ITEMS.id == items[1]).name,
        ITEMS.get(ITEMS.id == items[2]).name,
        ITEMS.get(ITEMS.id == items[3]).name,
        ITEMS.get(ITEMS.id == items[4]).name,
        ITEMS.get(ITEMS.id == items[5]).name,
    )


def set_runes(champion_num, index):
    rune = runes_champion_1[index] if champion_num == 1 else runes_champion_2[index]
    
    dict = {
        5011: "StatModsHealthScalingIcon.png",
        5002: "StatModsArmorIcon.png",
        5003: "StatModsMagicResIcon.png",
        5005: "StatModsAttackSpeedIcon.png",
        5007: "StatModsCDRScalingIcon.png",
        5008: "StatModsAdaptiveForceIcon.png",
        1: "StatModsAdaptiveForceScalingIcon.png",
        5001: "StatModsHealthPlusIcon.png",
        5010: "StatModsMovementSpeedIcon.png",
        5013: "StatModsTenacityIcon.png",
    }

    eel.set_title(champion_num, "runes", "Runes")
    eel.set_rune(
        champion_num,
        "primarystyle",
        "https://ddragon.leagueoflegends.com/cdn/img/"
        + RUNEKEYS.get(RUNEKEYS.id == rune["primaryStyle"]).icon,
    )

    eel.set_rune(
        champion_num,
        "primaryperk1",
        "https://ddragon.leagueoflegends.com/cdn/img/"
        + RUNES.get(RUNES.id == rune["primaryPerk1"]).icon,
    )
    eel.set_rune(
        champion_num,
        "primaryperk2",
        "https://ddragon.leagueoflegends.com/cdn/img/"
        + RUNES.get(RUNES.id == rune["primaryPerk2"]).icon,
    )
    eel.set_rune(
        champion_num,
        "primaryperk3",
        "https://ddragon.leagueoflegends.com/cdn/img/"
        + RUNES.get(RUNES.id == rune["primaryPerk3"]).icon,
    )
    eel.set_rune(
        champion_num,
        "primaryperk4",
        "https://ddragon.leagueoflegends.com/cdn/img/"
        + RUNES.get(RUNES.id == rune["primaryPerk4"]).icon,
    )

    eel.set_rune(
        champion_num,
        "substyle",
        "https://ddragon.leagueoflegends.com/cdn/img/"
        + RUNEKEYS.get(RUNEKEYS.id == rune["subStyle"]).icon,
    )

    eel.set_rune(
        champion_num,
        "subperk1",
        "https://ddragon.leagueoflegends.com/cdn/img/"
        + RUNES.get(RUNES.id == rune["subPerk1"]).icon,
    )
    eel.set_rune(
        champion_num,
        "subperk2",
        "https://ddragon.leagueoflegends.com/cdn/img/"
        + RUNES.get(RUNES.id == rune["subPerk2"]).icon,
    )

    eel.set_rune(
        champion_num,
        "offense",
        "https://ddragon.leagueoflegends.com/cdn/img/perk-images/StatMods/"
        + dict[rune["offense"]],
    )
    eel.set_rune(
        champion_num,
        "flex",
        "https://ddragon.leagueoflegends.com/cdn/img/perk-images/StatMods/"
        + dict[rune["flex"]],
    )
    eel.set_rune(
        champion_num,
        "defense",
        "https://ddragon.leagueoflegends.com/cdn/img/perk-images/StatMods/"
        + dict[rune["defense"]],
    )

    eel.set_rune_text(
        champion_num,
        RUNEKEYS.get(RUNEKEYS.id == rune["primaryStyle"]).name,
        RUNES.get(RUNES.id == rune["primaryPerk1"]).shortDesc,
        RUNES.get(RUNES.id == rune["primaryPerk2"]).shortDesc,
        RUNES.get(RUNES.id == rune["primaryPerk3"]).shortDesc,
        RUNES.get(RUNES.id == rune["primaryPerk4"]).shortDesc,
        RUNEKEYS.get(RUNEKEYS.id == rune["subStyle"]).name,
        RUNES.get(RUNES.id == rune["subPerk1"]).shortDesc,
        RUNES.get(RUNES.id == rune["subPerk2"]).shortDesc,
    )


def set_position(champion_num, position):
    eel.set_position(champion_num, position)


def start():
    try:
        eel.start(
            "quickplay.html",
            mode="chrome",
            host="localhost",
            port=27001,
            block=True,
            size=(1000, 850),
            position=(0, 0),
            disable_cache=True,
            close_callback=close_callback,
        )
    except EnvironmentError:
        eel.start(
            "quickplay.html",
            mode="default",
            host="localhost",
            port=27001,
            block=True,
            size=(1000, 850),
            position=(0, 0),
            disable_cache=True,
            close_callback=close_callback,
        )


def set_info_champion_1(
    champion, rune, summ, skills, position, items, start_items, boots, core_items
):
    global runes_champion_1
    runes_champion_1 = rune

    set_spells(1, champion)
    set_spell_order(1, champion, skills)
    set_summs(1, champion, summ)
    set_runes(1, 0)
    eel.init_rune(1)
    set_position(1, position)
    set_items(1, champion, items)
    set_start_items(1, champion, start_items)
    set_boots(1, champion, boots)
    set_core_items(1, champion, core_items)


def set_info_champion_2(
    champion, rune, summ, skills, position, items, start_items, boots, core_items
):
    global runes_champion_2
    runes_champion_2 = rune

    set_spells(2, champion)
    set_spell_order(2, champion, skills)
    set_summs(2, champion, summ)
    set_runes(2, 0)
    eel.init_rune(2)
    set_position(2, position)
    set_items(2, champion, items)
    set_start_items(2, champion, start_items)
    set_boots(2, champion, boots)
    set_core_items(2, champion, core_items)


@eel.expose
def update_runes(champion_num, index):
    try:
        # You'll need to modify lcu.py to handle champion_num for quickplay mode
        # For now, this is a placeholder
        run_coroutine_threadsafe(
            lcu.current_perks_delete(lcu.connector.connection), lcu.connector.loop
        )
        
        champion = lcu.champion  # This would need to be champion_1 or champion_2
        runes = runes_champion_1 if champion_num == 1 else runes_champion_2
        
        run_coroutine_threadsafe(
            lcu.set_perks(
                lcu.connector.connection,
                champion,
                runes[index],
                CHAMPIONS.get(CHAMPIONS.key == champion).champion,
            ),
            lcu.connector.loop,
        )
    except:
        pass

    set_runes(champion_num, index)


@eel.expose
def get_darkmode():
    return config.gui_darkmode


@eel.expose
def toggle_darkmode():
    if config.gui_darkmode:
        config.set_gui_darkmode(False)
    else:
        config.set_gui_darkmode(True)


@eel.expose
def get_import_runes():
    return config.import_runes


@eel.expose
def toggle_import_runes():
    if config.import_runes:
        config.set_import_runes(False)
    else:
        config.set_import_runes(True)


@eel.expose
def get_import_items():
    return config.import_items


@eel.expose
def toggle_import_items():
    if config.import_items:
        config.set_import_items(False)
    else:
        config.set_import_items(True)


@eel.expose
def get_import_summs():
    return config.import_summs


@eel.expose
def toggle_import_summs():
    if config.import_summs:
        config.set_import_summs(False)
    else:
        config.set_import_summs(True)


@eel.expose
def get_position_flash():
    return config.position_flash


@eel.expose
def toggle_position_flash():
    if config.position_flash == 0:
        config.set_position_flash(1)
    else:
        config.set_position_flash(0)


@eel.expose
def force_import():
    # Would need to handle both champions for quickplay
    run_coroutine_threadsafe(
        lcu.set_rune_summ_item(lcu.connector.connection, lcu.champion),
        lcu.connector.loop,
    )


@eel.expose
def force_position(champion_num, position):
    # Would need to handle both champions for quickplay
    run_coroutine_threadsafe(
        lcu.set_rune_summ_item(lcu.connector.connection, lcu.champion, position),
        lcu.connector.loop,
    )


def update_available(server_version, client_version):
    eel.update_available(server_version, client_version)
