from riotwatcher import LolWatcher, ApiError
from models.statics_db import CHAMPIONS, ITEMS, SUMMONER, MAPS, RUNEKEYS, RUNESLOTS, RUNES
import api_key

lol_watcher = LolWatcher(api_key.api_key)

def update_summoner():
    try:
        my_region = 'euw1'
        versions = lol_watcher.data_dragon.versions_for_region(my_region)
        summoner_version = versions['v']
        current_summoner_list = lol_watcher.data_dragon.summoner_spells(summoner_version)

        data = current_summoner_list['data']
        for item in data:

            if(not SUMMONER.get_or_none(SUMMONER.id == item)):
                SUMMONER.replace(
                    main_id = item,
                    cooldown = data[item]['cooldown'],
                    cooldownBurn = data[item]['cooldownBurn'],
                    cost = data[item]['cost'],
                    costBurn = data[item]['costBurn'],
                    costType = data[item]['costType'],
                    datavalues = data[item]['datavalues'],
                    description = data[item]['description'],
                    effect = data[item]['effect'],
                    effectBurn = data[item]['effectBurn'],
                    id = data[item]['id'],
                    image = data[item]['image'],
                    key = data[item]['key'],
                    maxammo = data[item]['maxammo'],
                    maxrank = data[item]['maxrank'],
                    modes = data[item]['modes'],
                    name = data[item]['name'],
                    range = data[item]['range'],
                    rangeBurn = data[item]['rangeBurn'],
                    resource = data[item]['resource'],
                    summonerLevel = data[item]['summonerLevel'],
                    tooltip = data[item]['tooltip'],
                    vars = data[item]['vars'],
                ).execute()



        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            raise

    print('Static Summoner')

def update_maps():
    try:
        my_region = 'euw1'
        versions = lol_watcher.data_dragon.versions_for_region(my_region)
        map_version = versions['v']
        current_map_list = lol_watcher.data_dragon.maps(map_version)

        data = current_map_list['data']
        for item in data:

            if(not MAPS.get_or_none(MAPS.id == item)):
                MAPS.replace(
                    id = item,
                    MapId = data[item]['MapId'],
                    MapName = data[item]['MapName'],
                    image = data[item]['image'],
                ).execute()



        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            raise

    print('Static Map')

def update_runes():
    try:
        my_region = 'euw1'
        versions = lol_watcher.data_dragon.versions_for_region(my_region)
        runes_reforged_version = versions['v']
        current_runes_reforged_list = lol_watcher.data_dragon.runes_reforged(runes_reforged_version)

        data = current_runes_reforged_list
        for item in data:
            slots = item['slots']
            for slot in slots:
                for rune in slot['runes']:
                    if(not RUNES.get_or_none(RUNES.id == rune['id'])):
                        RUNES.replace(
                            id = rune['id'],
                            icon = rune['icon'],
                            key = rune['key'],
                            longDesc = rune['longDesc'],
                            name = rune['name'],
                            shortDesc = rune['shortDesc'],
                        ).execute()

                if(not RUNESLOTS.get_or_none(RUNESLOTS.rune_1 == slot['runes'][0]['id'])):
                    RUNESLOTS.replace(
                        rune_1 = slot['runes'][0]['id'],
                        rune_2 = slot['runes'][1]['id'],
                        rune_3 = slot['runes'][2]['id'],
                    ).execute()

            if(not RUNEKEYS.get_or_none(RUNEKEYS.id == item['id'])):
                RUNEKEYS.replace(
                    id = item['id'],
                    icon = item['icon'],
                    key = item['key'],
                    name = item['name'],
                    slot_1 = slots[0]['runes'][0]['id'],
                    slot_2 = slots[1]['runes'][0]['id'],
                    slot_3 = slots[2]['runes'][0]['id'],
                    slot_4 = slots[3]['runes'][0]['id'],
                ).execute()



        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            raise

    print('Static Runes')

def update_items():
    try:
        my_region = 'euw1'
        versions = lol_watcher.data_dragon.versions_for_region(my_region)
        items_version = versions['v']
        current_item_list = lol_watcher.data_dragon.items(items_version)

        data = current_item_list['data']
        for item in data:
            try:
                depth = data[item]['depth']
            except:
                depth = 0

            try:
                effect = data[item]['effect']
            except:
                effect = 0
                
            try:
                from_ = data[item]['from']
            except:
                from_ = 0
                    
            try:
                stacks = data[item]['stacks']
            except:
                stacks = 0
                       
            try:
                into = data[item]['into']
            except:
                into = 0

            if(not ITEMS.get_or_none(ITEMS.id == item)):
                ITEMS.replace(
                    id = item,
                    colloq = data[item]['colloq'],
                    depth = depth,
                    description = data[item]['description'],
                    effect = effect,
                    from_ = from_,
                    gold = data[item]['gold'],
                    image = data[item]['image'],
                    into = into,
                    maps = data[item]['maps'],
                    name = data[item]['name'],
                    plaintext = data[item]['plaintext'],
                    stacks = stacks,
                    stats = data[item]['stats'],
                    tags = data[item]['tags'],
                ).execute()



        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            raise

    print('Static Items')

def update_champions():
    try:
        my_region = 'euw1'
        versions = lol_watcher.data_dragon.versions_for_region(my_region)
        champions_version = versions['v']
        current_champ_list = lol_watcher.data_dragon.champions(version=champions_version, full=True)

        data = current_champ_list['data']
        for champion in data:
            if(not CHAMPIONS.get_or_none(CHAMPIONS.champion == champion)):
                CHAMPIONS.replace(
                    champion = champion,
                    blurb = data[champion]['blurb'],
                    id = data[champion]['id'],

                    spell_image_passive = data[champion]['passive']['image']['full'],
                    spell_image_q = data[champion]['spells'][0]['image']['full'],
                    spell_image_w = data[champion]['spells'][1]['image']['full'],
                    spell_image_e = data[champion]['spells'][2]['image']['full'],
                    spell_image_r = data[champion]['spells'][3]['image']['full'],

                    spell_text_passive = data[champion]['passive']['description'],
                    spell_text_q = data[champion]['spells'][0]['description'],
                    spell_text_w = data[champion]['spells'][1]['description'],
                    spell_text_e = data[champion]['spells'][2]['description'],
                    spell_text_r = data[champion]['spells'][3]['description'],

                    image_full = data[champion]['image']['full'],
                    image_group = data[champion]['image']['group'],
                    image_h = data[champion]['image']['h'],
                    image_sprite = data[champion]['image']['sprite'],
                    image_w = data[champion]['image']['w'],
                    image_x = data[champion]['image']['x'],
                    image_y = data[champion]['image']['y'],

                    info_attack = data[champion]['info']['attack'],
                    info_defense = data[champion]['info']['defense'],
                    info_difficulty = data[champion]['info']['difficulty'],
                    info_magic = data[champion]['info']['magic'],

                    key = data[champion]['key'],
                    name = data[champion]['name'],
                    partype = data[champion]['partype'],

                    stats_armor = data[champion]['stats']['armor'],
                    stats_armorperlevel = data[champion]['stats']['armorperlevel'],
                    stats_attackdamage = data[champion]['stats']['attackdamage'],
                    stats_attackdamageperlevel = data[champion]['stats']['attackdamageperlevel'],
                    stats_attackrange = data[champion]['stats']['attackrange'],
                    stats_attackspeed = data[champion]['stats']['attackspeed'],
                    stats_attackspeedperlevel = data[champion]['stats']['attackspeedperlevel'],
                    stats_crit = data[champion]['stats']['crit'],
                    stats_critperlevel = data[champion]['stats']['critperlevel'],
                    stats_hp = data[champion]['stats']['hp'],
                    stats_hpperlevel = data[champion]['stats']['hpperlevel'],
                    stats_hpregen = data[champion]['stats']['hpregen'],
                    stats_hpregenperlevel = data[champion]['stats']['hpregenperlevel'],
                    stats_movespeed = data[champion]['stats']['movespeed'],
                    stats_mp = data[champion]['stats']['mp'],
                    stats_mpperlevel = data[champion]['stats']['mpperlevel'],
                    stats_mpregen = data[champion]['stats']['mpregen'],
                    stats_mpregenperlevel = data[champion]['stats']['mpregenperlevel'],
                    stats_spellblock = data[champion]['stats']['spellblock'],
                    stats_spellblockperlevel = data[champion]['stats']['spellblockperlevel'],

                    tags = data[champion]['tags'],
                    title = data[champion]['title'],
                    version = champions_version,
                ).execute()



        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            raise

    print('Static Champion')