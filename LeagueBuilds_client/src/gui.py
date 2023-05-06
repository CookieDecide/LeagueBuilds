import eel
import sys

from models.statics_db import RUNES, RUNEKEYS, SUMMONER, CHAMPIONS, ITEMS
import config

from asyncio import run_coroutine_threadsafe
import lcu

runes = []

def close_callback(route, websockets):
    if not websockets:
        sys.exit()

eel.init('web')

def set_spells(champion):
    eel.set_title('spells', 'Spells')

    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_champion_img('champion', 'https://ddragon.leagueoflegends.com/cdn/img/champion/loading/'+ entry.champion +'_0.jpg')

    eel.set_spell_img('img_passive', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/passive/' + entry.spell_image_passive)
    eel.set_spell_img('img_Q', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + entry.spell_image_q)
    eel.set_spell_img('img_W', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + entry.spell_image_w)
    eel.set_spell_img('img_E', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + entry.spell_image_e)
    eel.set_spell_img('img_R', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + entry.spell_image_r)

    eel.set_spell_text(entry.spell_text_passive,
                        entry.spell_text_q,
                        entry.spell_text_w,
                        entry.spell_text_e,
                        entry.spell_text_r)

    eel.set_spell_src(  "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_P1.webm".format(championId = champion),
                        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_Q1.webm".format(championId = champion),
                        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_W1.webm".format(championId = champion),
                        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_E1.webm".format(championId = champion),
                        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_R1.webm".format(championId = champion))

def set_spell_order(champion, skills):
    dict = {1:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_q, 2:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_w, 3:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_e, 4:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_r}
    spell_key = {1: 'Q', 2: 'W', 3: 'E', 4: 'R'}

    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version
    
    eel.set_title('spell-order', 'Spell-order')
    eel.set_spell_name('skill-1-name', skills[0])
    eel.set_spell_order('skill-1', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + dict[skills[0]])
    eel.set_spell_name('skill-2-name', skills[1])
    eel.set_spell_order('skill-2', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + dict[skills[1]])
    eel.set_spell_name('skill-3-name', skills[2])
    eel.set_spell_order('skill-3', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + dict[skills[2]])
    eel.set_spell_name('skill-4-name', skills[3])
    eel.set_spell_order('skill-4', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + dict[skills[3]])
    eel.set_spell_name('skill-5-name', skills[4])
    eel.set_spell_order('skill-5', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + dict[skills[4]])
    eel.set_spell_name('skill-6-name', skills[5])
    eel.set_spell_order('skill-6', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + dict[skills[5]])
    eel.set_spell_name('skill-7-name', skills[6])
    eel.set_spell_order('skill-7', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + dict[skills[6]])
    eel.set_spell_name('skill-8-name', skills[7])
    eel.set_spell_order('skill-8', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + dict[skills[7]])

def set_summs(champion, summ):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_title('summoner-spells', 'Summoner Spells')
    eel.set_summ('summ-1', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + SUMMONER.get(SUMMONER.key == summ[0]).id + '.png')
    eel.set_summ('summ-2', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/spell/' + SUMMONER.get(SUMMONER.key == summ[1]).id + '.png')

    eel.set_summ_text(SUMMONER.get(SUMMONER.key == summ[0]).description,
                        SUMMONER.get(SUMMONER.key == summ[1]).description)
    
def set_items(champion, items):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_title('items', 'Builds')
    eel.set_item('item1', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[0][0]).id + '.png')
    eel.set_item('item2', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[0][1]).id + '.png')
    eel.set_item('item3', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[0][2]).id + '.png')

    eel.set_item('item4', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[1][0]).id + '.png')
    eel.set_item('item5', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[1][1]).id + '.png')
    eel.set_item('item6', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[1][2]).id + '.png')

    eel.set_item('item7', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[2][0]).id + '.png')
    eel.set_item('item8', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[2][1]).id + '.png')
    eel.set_item('item9', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[2][2]).id + '.png')

    eel.set_item_text(ITEMS.get(ITEMS.id == items[0][0]).name,
                        ITEMS.get(ITEMS.id == items[0][1]).name,
                        ITEMS.get(ITEMS.id == items[0][2]).name,
                        ITEMS.get(ITEMS.id == items[1][0]).name,
                        ITEMS.get(ITEMS.id == items[1][1]).name,
                        ITEMS.get(ITEMS.id == items[1][2]).name,
                        ITEMS.get(ITEMS.id == items[2][0]).name,
                        ITEMS.get(ITEMS.id == items[2][1]).name,
                        ITEMS.get(ITEMS.id == items[2][2]).name)
    
def set_start_items(champion, items):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_title('start-items', 'Start Items')
    for i in range(len(items[0])):
        eel.set_item('start-item'+str(i+1), 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[0][i]).id + '.png')

    names = [(ITEMS.get(ITEMS.id == items[0][i]).name) for i in range(len(items[0]))]
    for i in range(len(items[0]),3):
        names.append("")

    eel.set_start_item_text(names[0],
                      names[1],
                      names[2])
    
def set_boots(champion, items):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    eel.set_title('boots', 'Boots')
    eel.set_item('boots1', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[0]).id + '.png')
    eel.set_item('boots2', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[1]).id + '.png')
    eel.set_item('boots3', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[2]).id + '.png')

    eel.set_boots_text(ITEMS.get(ITEMS.id == items[0]).name,
                      ITEMS.get(ITEMS.id == items[1]).name,
                      ITEMS.get(ITEMS.id == items[2]).name)
    
def set_core_items(champion, items):
    entry = CHAMPIONS.get(CHAMPIONS.key == champion)
    version = entry.version

    for item in [0,1054,1055,1056]:
        try:
            items.remove(item)
        except:
            pass

    eel.set_title('core-items', 'Core Items')
    eel.set_item('core-item1', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[0]).id + '.png')
    eel.set_item('core-item2', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[1]).id + '.png')
    eel.set_item('core-item3', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[2]).id + '.png')
    eel.set_item('core-item4', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[3]).id + '.png')
    eel.set_item('core-item5', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[4]).id + '.png')
    eel.set_item('core-item6', 'https://ddragon.leagueoflegends.com/cdn/' + version + '/img/item/' + ITEMS.get(ITEMS.id == items[5]).id + '.png')

    eel.set_core_item_text(ITEMS.get(ITEMS.id == items[0]).name,
                      ITEMS.get(ITEMS.id == items[1]).name,
                      ITEMS.get(ITEMS.id == items[2]).name,
                      ITEMS.get(ITEMS.id == items[3]).name,
                      ITEMS.get(ITEMS.id == items[4]).name,
                      ITEMS.get(ITEMS.id == items[5]).name)

def set_runes(index):
    rune = runes[index]
    dict = {5001:'StatModsHealthScalingIcon.png', 5002:'StatModsArmorIcon.png', 5003:'StatModsMagicResIcon.png', 5005:'StatModsAttackSpeedIcon.png', 5007:'StatModsCDRScalingIcon.png', 5008:'StatModsAdaptiveForceIcon.png'}

    eel.set_title('runes', 'Runes')
    eel.set_rune('primarystyle', 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNEKEYS.get(RUNEKEYS.id == rune['primaryStyle']).icon)

    eel.set_rune('primaryperk1', 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['primaryPerk1']).icon)
    eel.set_rune('primaryperk2', 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['primaryPerk2']).icon)
    eel.set_rune('primaryperk3', 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['primaryPerk3']).icon)
    eel.set_rune('primaryperk4', 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['primaryPerk4']).icon)

    eel.set_rune('substyle', 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNEKEYS.get(RUNEKEYS.id == rune['subStyle']).icon)

    eel.set_rune('subperk1', 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['subPerk1']).icon)
    eel.set_rune('subperk2', 'https://ddragon.leagueoflegends.com/cdn/img/' + RUNES.get(RUNES.id == rune['subPerk2']).icon)

    eel.set_rune('offense', 'https://ddragon.leagueoflegends.com/cdn/img/perk-images/StatMods/' + dict[rune['offense']])
    eel.set_rune('flex', 'https://ddragon.leagueoflegends.com/cdn/img/perk-images/StatMods/' + dict[rune['flex']])
    eel.set_rune('defense', 'https://ddragon.leagueoflegends.com/cdn/img/perk-images/StatMods/' + dict[rune['defense']])

    eel.set_rune_text(RUNEKEYS.get(RUNEKEYS.id == rune['primaryStyle']).name,
                        RUNES.get(RUNES.id == rune['primaryPerk1']).shortDesc,
                        RUNES.get(RUNES.id == rune['primaryPerk2']).shortDesc,
                        RUNES.get(RUNES.id == rune['primaryPerk3']).shortDesc,
                        RUNES.get(RUNES.id == rune['primaryPerk4']).shortDesc,
                        RUNEKEYS.get(RUNEKEYS.id == rune['subStyle']).name,
                        RUNES.get(RUNES.id == rune['subPerk1']).shortDesc,
                        RUNES.get(RUNES.id == rune['subPerk2']).shortDesc)

def set_position(position):
    eel.set_position(position)

def start():
    try:
        print('start')
        eel.start('index.html', mode='chrome',
                                host='localhost', 
                                port=27000, 
                                block=True, 
                                size=(1000, 850), 
                                position=(0,0), 
                                disable_cache=True, 
                                close_callback=close_callback,
                                )
    except EnvironmentError:
        print('exe')
        eel.start('index.html', mode='default', 
                                host='localhost', 
                                port=27000, 
                                block=True, 
                                size=(1000, 850), 
                                position=(0,0), 
                                disable_cache=True, 
                                close_callback=close_callback,
                                )

def set_info(champion, rune, summ, skills, position, items, start_items, boots, core_items):
    global runes
    runes = rune

    set_spells(champion)
    set_spell_order(champion, skills)
    set_summs(champion, summ)
    set_runes(0)
    eel.init_rune()
    set_position(position)
    set_items(champion, items)
    set_start_items(champion, start_items)
    set_boots(champion, boots)
    set_core_items(champion, core_items)

@eel.expose
def update_runes(index):
    try:
        run_coroutine_threadsafe(lcu.current_perks_delete(lcu.connector.connection), lcu.connector.loop)
        run_coroutine_threadsafe(lcu.set_perks(lcu.connector.connection, lcu.champion, runes[index], CHAMPIONS.get(CHAMPIONS.key == lcu.champion).champion), lcu.connector.loop)
    except:
        pass
    
    set_runes(index)

@eel.expose
def get_darkmode():
    return config.gui_darkmode
@eel.expose
def toggle_darkmode():
    if(config.gui_darkmode):
        config.set_gui_darkmode(False)
    else:
        config.set_gui_darkmode(True)

@eel.expose
def get_import_runes():
    return config.import_runes
@eel.expose
def toggle_import_runes():
    if(config.import_runes):
        config.set_import_runes(False)
    else:
        config.set_import_runes(True)

@eel.expose
def get_import_items():
    return config.import_items
@eel.expose
def toggle_import_items():
    if(config.import_items):
        config.set_import_items(False)
    else:
        config.set_import_items(True)

@eel.expose
def get_import_summs():
    return config.import_summs
@eel.expose
def toggle_import_summs():
    if(config.import_summs):
        config.set_import_summs(False)
    else:
        config.set_import_summs(True)

@eel.expose
def get_position_flash():
    return config.position_flash
@eel.expose
def toggle_position_flash():
    if(config.position_flash == 0):
        config.set_position_flash(1)
    else:
        config.set_position_flash(0)

@eel.expose
def force_import():
    run_coroutine_threadsafe(lcu.set_rune_summ_item(lcu.connector.connection, lcu.champion), lcu.connector.loop)

@eel.expose
def force_position(position):
    run_coroutine_threadsafe(lcu.set_rune_summ_item(lcu.connector.connection, lcu.champion, position), lcu.connector.loop)

def update_available(server_version, client_version):
    eel.update_available(server_version, client_version)