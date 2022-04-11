from models.statics_db import CHAMPIONS
import json, sorting, datetime

from lcu_driver import Connector

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
        champion = json.loads(page)

        if(champion != 0):
            await set_rune_summ_item(connection, champion)

@connector.close
async def disconnect(_):
    print('The client has been closed!')
    await connector.stop()

@connector.ws.register('/lol-champ-select/v1/current-champion', event_types=['CREATE', 'UPDATE'])
async def on_champion_selected(connection, event):
    champion = event.data

    await set_rune_summ_item(connection, champion)

@connector.ws.register('/lol-champ-select/v1/session', event_types=['UPDATE'])
async def on_champion_selected(connection, event):
    global old_action
    localPlayerCellId = event.data['localPlayerCellId']

    for action in event.data['actions'][0]:
        champion = action['championId']
        actorCellId = action['actorCellId']
        
        if(action['type'] == 'pick'):
            if(actorCellId == localPlayerCellId):
                if(action != old_action):
                    old_action = action
                    if(champion != 0):
                        await set_rune_summ_item(connection, champion)

async def set_rune_summ_item(connection, champion):
    start = datetime.datetime.now()
    
    print(CHAMPIONS.get(CHAMPIONS.key == str(champion)).name)

    page = await connection.request('get', '/lol-champ-select/v1/session')
    page = await page.content.read()
    summoner = json.loads(page)
    localPlayerCellId = summoner['localPlayerCellId']

    page = await connection.request('get', '/lol-champ-select/v1/summoners/' + str(localPlayerCellId))
    page = await page.content.read()
    summoner = json.loads(page)
    position = summoner['assignedPosition']

    rune,summ,item,start_item,item_build,skills = sorting.info(champion, position)

    skill_order(skills)

    page = await connection.request('get', '/lol-summoner/v1/current-summoner/account-and-summoner-ids')
    page = await page.content.read()
    accountId = json.loads(page)['accountId']
    summonerId = json.loads(page)['summonerId']

    page = await connection.request('get', '/lol-perks/v1/currentpage')
    page = await page.content.read()
    page_id = json.loads(page)['id']

    page = await connection.request('delete', '/lol-perks/v1/pages/'+str(page_id))

    body = {
    "name":CHAMPIONS.get(CHAMPIONS.key == str(champion)).name,
    "primaryStyleId":rune['primaryStyle'],
    "subStyleId":rune['subStyle'],     
    "selectedPerkIds": [rune['primaryPerk1'],rune['primaryPerk2'],rune['primaryPerk3'],rune['primaryPerk4'],rune['subPerk1'],rune['subPerk2'],rune['offense'],rune['flex'],rune['defense']],
    "current":True,
    }
    page = await connection.request('post', '/lol-perks/v1/pages', data = body)

    body = {
    'spell1Id' : str(summ[0]),
    'spell2Id' : str(summ[1])
    }
    page = await connection.request('patch', '/lol-champ-select/v1/session/my-selection', data = body)

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
                "title": CHAMPIONS.get(CHAMPIONS.key == str(champion)).name,
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
    
    for liste in item_build:
        body['itemSets'][0]['blocks'].append(get_block(("Build " + str(id))))
        for i in liste:
            body['itemSets'][0]['blocks'][id]['items'].append({'count': 1, 'id': str(i)})
        id += 1

    body['itemSets'][0]['blocks'].append(get_block("Items"))
    for i in item:
        body['itemSets'][0]['blocks'][id]['items'].append({'count': 1, 'id': str(i)})
    id += 1

    page = await connection.request('put', '/lol-item-sets/v1/item-sets/' + str(summonerId) + '/sets', data = body)

    print(datetime.datetime.now() - start)

def get_block(name):
    block = {
        "hideIfSummonerSpell": "",
        "items": [],
        "showIfSummonerSpell": "",
        "type": str(name)
    }
    return block

def skill_order(skills):
    msg = ''
    for skill in skills:
        if(skill == 1):
            msg += 'Q->'
        elif(skill == 2):
            msg += 'W->'
        elif(skill == 3):
            msg += 'E->'
    
    print(msg[:-2])