from threading import local
from models.statics_db import CHAMPIONS
import json, sorting

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
        
        if(action['type'] != 'ban'):
            if(actorCellId == localPlayerCellId):
                if(action != old_action):
                    old_action = action
                    if(champion != 0):
                        await set_rune_summ_item(connection, champion)

async def set_rune_summ_item(connection, champion):
    print(CHAMPIONS.get(CHAMPIONS.key == str(champion)).name)

    page = await connection.request('get', '/lol-champ-select/v1/session')
    page = await page.content.read()
    summoner = json.loads(page)
    localPlayerCellId = summoner['localPlayerCellId']

    page = await connection.request('get', '/lol-champ-select/v1/summoners/' + str(localPlayerCellId))
    page = await page.content.read()
    summoner = json.loads(page)
    position = summoner['assignedPosition']

    rune,summ,item = sorting.info(champion, position)

    page = await connection.request('get', '/lol-summoner/v1/current-summoner')
    page = await page.content.read()
    summonerId = json.loads(page)['summonerId']
    accountId = json.loads(page)['accountId']

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
                "blocks": [
                    {
                        "hideIfSummonerSpell": "",
                        "items": [],
                        "showIfSummonerSpell": "",
                        "type": "Items"
                    }
                ],
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
    for i in item:
        body['itemSets'][0]['blocks'][0]['items'].append({'count': 1, 'id': str(i)})

    page = await connection.request('put', '/lol-item-sets/v1/item-sets/' + str(summonerId) + '/sets', data = body)