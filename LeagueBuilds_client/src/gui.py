import eel
import sys

from models.statics_db import RUNES, RUNEKEYS, SUMMONER, CHAMPIONS
import config

def close_callback(route, websockets):
    if not websockets:
        sys.exit()

eel.init('web')

def set_spells(champion):
    eel.set_title('spells', 'Spells')

    eel.set_spell_img('img_passive', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/passive/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_passive)
    eel.set_spell_img('img_Q', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_q)
    eel.set_spell_img('img_W', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_w)
    eel.set_spell_img('img_E', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_e)
    eel.set_spell_img('img_R', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_r)

    eel.set_spell_text(CHAMPIONS.get(CHAMPIONS.key == champion).spell_text_passive,
                        CHAMPIONS.get(CHAMPIONS.key == champion).spell_text_q,
                        CHAMPIONS.get(CHAMPIONS.key == champion).spell_text_w,
                        CHAMPIONS.get(CHAMPIONS.key == champion).spell_text_e,
                        CHAMPIONS.get(CHAMPIONS.key == champion).spell_text_r)

    eel.set_spell_src(  "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_P1.webm".format(championId = champion),
                        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_Q1.webm".format(championId = champion),
                        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_W1.webm".format(championId = champion),
                        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_E1.webm".format(championId = champion),
                        "https://d28xe8vt774jo5.cloudfront.net/champion-abilities/{championId:0>4}/ability_{championId:0>4}_R1.webm".format(championId = champion))

def set_spell_order(champion, skills):
    dict = {1:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_q, 2:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_w, 3:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_e, 4:CHAMPIONS.get(CHAMPIONS.key == champion).spell_image_r}
    spell_key = {1: 'Q', 2: 'W', 3: 'E', 4: 'R'}
    
    eel.set_title('spell-order', 'Spell-order')
    eel.set_title('skill-1-name', spell_key[skills[0]])
    eel.set_spell_order('skill-1', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[0]])
    eel.set_title('skill-2-name', spell_key[skills[1]])
    eel.set_spell_order('skill-2', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[1]])
    eel.set_title('skill-3-name', spell_key[skills[2]])
    eel.set_spell_order('skill-3', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[2]])
    eel.set_title('skill-4-name', spell_key[skills[3]])
    eel.set_spell_order('skill-4', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[3]])
    eel.set_title('skill-5-name', spell_key[skills[4]])
    eel.set_spell_order('skill-5', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[4]])
    eel.set_title('skill-6-name', spell_key[skills[5]])
    eel.set_spell_order('skill-6', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[5]])
    eel.set_title('skill-7-name', spell_key[skills[6]])
    eel.set_spell_order('skill-7', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[6]])
    eel.set_title('skill-8-name', spell_key[skills[7]])
    eel.set_spell_order('skill-8', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[7]])
    '''
    eel.set_title('skill-9-name', spell_key[skills[8]])
    eel.set_spell_order('skill-9', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[8]])
    eel.set_title('skill-10-name', spell_key[skills[9]])
    eel.set_spell_order('skill-10', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[9]])
    eel.set_title('skill-11-name', spell_key[skills[10]])
    eel.set_spell_order('skill-11', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[10]])
    eel.set_title('skill-12-name', spell_key[skills[11]])
    eel.set_spell_order('skill-12', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[11]])
    eel.set_title('skill-13-name', spell_key[skills[12]])
    eel.set_spell_order('skill-13', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[12]])
    eel.set_title('skill-14-name', spell_key[skills[13]])
    eel.set_spell_order('skill-14', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[13]])
    eel.set_title('skill-15-name', spell_key[skills[14]])
    eel.set_spell_order('skill-15', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[14]])
    eel.set_title('skill-16-name', spell_key[skills[15]])
    eel.set_spell_order('skill-16', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[15]])
    eel.set_title('skill-17-name', spell_key[skills[16]])
    eel.set_spell_order('skill-17', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[16]])
    eel.set_title('skill-18-name', spell_key[skills[17]])
    eel.set_spell_order('skill-18', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + dict[skills[17]])
    '''

def set_summs(summ):
    eel.set_title('summoner-spells', 'Summoner Spells')
    eel.set_summ('summ-1', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + SUMMONER.get(SUMMONER.key == summ[0]).id + '.png')
    eel.set_summ('summ-2', 'https://ddragon.leagueoflegends.com/cdn/12.6.1/img/spell/' + SUMMONER.get(SUMMONER.key == summ[1]).id + '.png')

    eel.set_summ_text(SUMMONER.get(SUMMONER.key == summ[0]).description,
                        SUMMONER.get(SUMMONER.key == summ[1]).description)

def set_runes(rune):
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

def start():
    try:
        print('start')
        eel.start('index.html', mode='chrome',
                                host='localhost', 
                                port=27000, 
                                block=True, 
                                size=(320, 950), 
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
                                size=(320, 950), 
                                position=(0,0), 
                                disable_cache=True, 
                                close_callback=close_callback,
                                )

def set_info(champion, rune, summ, skills):
    set_spells(champion)
    set_spell_order(champion, skills)
    set_summs(summ)
    set_runes(rune)

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