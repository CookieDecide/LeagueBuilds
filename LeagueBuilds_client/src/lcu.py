import json, client, datetime, config
import gui

from lcu_driver import Connector

champion, rune, summ, skills = None, None, None, None

old_action = None
connector = Connector()

def start():
    print('Please start LoL client for LCU API to start.')
    connector.start()

@connector.ready
async def connect(connection):
    print('LCU API is ready to be used.')
    page = await connection.request('get', '/lol-champ-select/v1/session')
    page = await page.content.read()

    if('errorCode' not in json.loads(page)):
        page = await connection.request('get', '/lol-champ-select/v1/current-champion')
        page = await page.content.read()
        champ = json.loads(page)

        if(champ != 0):
            champion = champ
            await set_rune_summ_item(connection, champion)

@connector.close
async def disconnect(_):
    print('The client has been closed!')

@connector.ws.register('/lol-champ-select/v1/current-champion', event_types=['CREATE', 'UPDATE'])
async def on_champion_selected(connection, event):
    global champion

    if(event.data != champion):
        champion = event.data

        await set_rune_summ_item(connection, champion)

@connector.ws.register('/lol-champ-select/v1/session', event_types=['CREATE', 'UPDATE'])
async def on_session_changed(connection, event):
    global old_action, champion
    localPlayerCellId = event.data['localPlayerCellId']

    for actions in event.data['actions']:
        for action in actions:
            champ = action['championId']
            actorCellId = action['actorCellId']
            
            if(action['type'] == 'pick'):
                if(actorCellId == localPlayerCellId):
                    if(event.data['actions'] != old_action):
                        old_action = event.data['actions']
                        if(champ != 0 and champ != champion):
                            champion = champ
                            await set_rune_summ_item(connection, champion)

async def set_rune_summ_item(connection, champion):
    start = datetime.datetime.now()

    localPlayerCellId = await get_localPlayerCellId(connection)

    if (await is_aram(connection)):
        position = 'aram'
    else:
        position = await get_position(connection, localPlayerCellId)

    global rune, summ, skills

    championId,rune,summ,item,start_item,item_build,skills,position,champion_name, boots = client.get_build(champion, position)

    print(champion_name)

    accountId, summonerId = await get_acc_sum_id(connection)

    if(config.import_runes):
        await current_perks_delete(connection)
        await set_perks(connection, champion, rune, champion_name)

    if(config.import_summs):
        await set_summs(connection, summ)

    if(config.import_items):
        await set_itemset(connection, accountId, summonerId, champion, start_item, item_build, item, champion_name, boots)

    print(datetime.datetime.now() - start)
    gui.set_info(championId,rune,summ,skills)

def get_block(name):
    block = {
        "hideIfSummonerSpell": "",
        "items": [],
        "showIfSummonerSpell": "",
        "type": str(name)
    }
    return block

async def set_itemset(connection, accountId, summonerId, champion, start_item, item_build, item, champion_name, boots):
    body = {
        "accountId": accountId,
        "itemSets": [
            {
                "associatedChampions": [champion],
                "associatedMaps": [],
                "blocks": [],
                "map": "any",
                "mode": "any",
                "preferredItemSlots": [],
                "sortrank": 1,
                "startedFrom": "blank",
                "title": champion_name,
                "type": "custom",
                "uid": "1"
            }
        ],
        "timestamp": 0
    }

    id = 0
    for liste in start_item:
        body['itemSets'][0]['blocks'].append(get_block("Start Items"))
        for i in liste:
            body['itemSets'][0]['blocks'][id]['items'].append({'count': 1, 'id': str(i)})
        id += 1

    body['itemSets'][0]['blocks'].append(get_block("Boots"))
    for i in boots:
        body['itemSets'][0]['blocks'][id]['items'].append({'count': 1, 'id': str(i)})
    id += 1
    
    for liste in item_build:
        body['itemSets'][0]['blocks'].append(get_block(("Build " + str(id-3))))
        for i in liste:
            body['itemSets'][0]['blocks'][id]['items'].append({'count': 1, 'id': str(i)})
        id += 1

    body['itemSets'][0]['blocks'].append(get_block("Items"))
    for i in item:
        body['itemSets'][0]['blocks'][id]['items'].append({'count': 1, 'id': str(i)})
    id += 1

    return await connection.request('put', '/lol-item-sets/v1/item-sets/' + str(summonerId) + '/sets', data = body)

async def set_perks(connection, champion, rune, champion_name):
    body = {
    "name":champion_name,
    "primaryStyleId":rune['primaryStyle'],
    "subStyleId":rune['subStyle'],     
    "selectedPerkIds": [rune['primaryPerk1'],rune['primaryPerk2'],rune['primaryPerk3'],rune['primaryPerk4'],rune['subPerk1'],rune['subPerk2'],rune['offense'],rune['flex'],rune['defense']],
    "current":True,
    }
    return await connection.request('post', '/lol-perks/v1/pages', data = body)

async def set_summs(connection, summ):
    if(4 in summ):
        if(config.position_flash == 0 and summ[1] == 4):
            summ[1] = summ[0]
            summ[0] = 4
        elif(config.position_flash == 1 and summ[0] == 4):
            summ[0] = summ[1]
            summ[1] = 4
            
    body = {
    'spell1Id' : str(summ[0]),
    'spell2Id' : str(summ[1])
    }
    return await connection.request('patch', '/lol-champ-select/v1/session/my-selection', data = body)

async def current_perks_delete(connection):
    page = await connection.request('get', '/lol-perks/v1/currentpage')
    page = await page.content.read()
    page_id = json.loads(page)['id']

    return await connection.request('delete', '/lol-perks/v1/pages/'+str(page_id))

async def get_acc_sum_id(connection):
    page = await connection.request('get', '/lol-summoner/v1/current-summoner/account-and-summoner-ids')
    page = await page.content.read()
    accountId = json.loads(page)['accountId']
    summonerId = json.loads(page)['summonerId']

    return accountId, summonerId

async def get_localPlayerCellId(connection):
    page = await connection.request('get', '/lol-champ-select/v1/session')
    page = await page.content.read()
    summoner = json.loads(page)
    return summoner['localPlayerCellId']

async def get_position(connection, localPlayerCellId):
    page = await connection.request('get', '/lol-champ-select/v1/summoners/' + str(localPlayerCellId))
    page = await page.content.read()
    summoner = json.loads(page)
    return summoner['assignedPosition']

async def is_aram(connection):
    page = await connection.request('get', '/lol-champ-select/v1/session')
    page = await page.content.read()
    page = json.loads(page)

    if(page['allowBattleBoost'] == True and page['allowRerolling'] == True and page['benchEnabled'] == True):
        return True
    
    return False


def get_champion():
    return champion

def get_rune():
    return rune

def get_summ():
    return summ

def get_skills():
    return skills