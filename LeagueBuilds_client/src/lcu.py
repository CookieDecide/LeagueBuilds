import json, client, datetime, config
import gui

from lcu_driver import Connector

champion, rune, summ, skills, quickplay_1, quickplay_2 = None, None, None, None, None, None

old_action = None
connector = Connector()


def start():
    # print("Please start LoL client for LCU API to start.")
    connector.start()


@connector.ready
async def connect(connection):
    global old_action, champion
    # print("LCU API is ready to be used.")
    page_session = await connection.request("get", "/lol-champ-select/v1/session")
    page_session = await page_session.content.read()
    page_session = json.loads(page_session)

    if "errorCode" not in page_session:
        page = await connection.request("get", "/lol-champ-select/v1/current-champion")
        page = await page.content.read()
        champ = json.loads(page)

        if champ != 0:
            champion = champ
            await set_rune_summ_item(connection, champion)

        localPlayerCellId = page_session["localPlayerCellId"]

        for actions in page_session["actions"]:
            for action in actions:
                champ = action["championId"]
                actorCellId = action["actorCellId"]

                if action["type"] == "pick":
                    if actorCellId == localPlayerCellId:
                        if page_session["actions"] != old_action:
                            old_action = page_session["actions"]
                            if champ != 0 and champ != champion:
                                champion = champ


@connector.close
async def disconnect(_):
    # print("The client has been closed!")
    return


@connector.ws.register(
    "/lol-champ-select/v1/current-champion", event_types=["CREATE", "UPDATE"]
)
async def on_champion_selected(connection, event):
    global champion

    if event.data != champion:
        champion = event.data

        await set_rune_summ_item(connection, champion)


@connector.ws.register("/lol-champ-select/v1/session", event_types=["CREATE", "UPDATE"])
async def on_session_changed(connection, event):
    global old_action, champion
    localPlayerCellId = event.data["localPlayerCellId"]

    for actions in event.data["actions"]:
        for action in actions:
            champ = action["championId"]
            actorCellId = action["actorCellId"]

            if action["type"] == "pick":
                if actorCellId == localPlayerCellId:
                    if event.data["actions"] != old_action:
                        old_action = event.data["actions"]
                        if champ != 0 and champ != champion:
                            champion = champ
                            await set_rune_summ_item(connection, champion)


@connector.ws.register("/lol-settings/v2/account/LCUPreferences/lol-quick-play", event_types=["UPDATE"])
async def on_quick_play(connection, event):
    try:
        page = await connection.request("get", "/lol-lobby/v2/lobby")
        page = json.loads(await page.content.read())

        if( page["gameConfig"]["queueId"] != 480 ):
            return
    except:
        return

    global quickplay_1, quickplay_2
    print("Event Quick-Play")

    page = await connection.request("delete", "/lol-perks/v1/pages")

    page = await connection.request("get", "/lol-settings/v2/account/LCUPreferences/lol-quick-play")
    page = await page.content.read()

    page_id = json.loads(page)

    try:
        championId_1 = page_id["data"]["slotsByQueueId"]["480"][0]["championId"]
        championId_2 = page_id["data"]["slotsByQueueId"]["480"][1]["championId"]

        position_1 = page_id["data"]["slotsByQueueId"]["480"][0]["positionPreference"]
        position_2 = page_id["data"]["slotsByQueueId"]["480"][1]["positionPreference"]

        if championId_1 != 0 and position_1 != "":
            (
            championId_1,
            rune_1,
            summ_1,
            item_1,
            start_item_1,
            item_build_1,
            skills_1,
            position_1,
            champion_name_1,
            boots_1,
            ) = client.get_build(championId_1, position_1, await get_summoner_name(connection))

        if championId_2 != 0 and position_2 != "":
            (
            championId_2,
            rune_2,
            summ_2,
            item_2,
            start_item_2,
            item_build_2,
            skills_2,
            position_2,
            champion_name_2,
            boots_2,
            ) = client.get_build(championId_2, position_2, await get_summoner_name(connection))

        if isinstance(rune_1, dict):
            rune_1 = [rune_1, rune_1, rune_1]

        if isinstance(rune_2, dict):
            rune_2 = [rune_2, rune_2, rune_2]

        print(champion_name_1)
        print(champion_name_2)

        accountId, summonerId = await get_acc_sum_id(connection)

        if config.import_runes:
            await connection.request("delete", "/lol-perks/v1/pages")

            await set_perks(connection, championId_1, rune_1[0], champion_name_1)
            await set_perks(connection, championId_2, rune_2[0], champion_name_2)

            body_1 = {
                "championId": championId_1,
                "perks": json.dumps(
                    {
                        "perkIds": [
                            rune_1[0]["primaryPerk1"],
                            rune_1[0]["primaryPerk2"],
                            rune_1[0]["primaryPerk3"],
                            rune_1[0]["primaryPerk4"],
                            rune_1[0]["subPerk1"],
                            rune_1[0]["subPerk2"],
                            rune_1[0]["offense"],
                            rune_1[0]["flex"],
                            rune_1[0]["defense"],
                        ],
                        "perkStyle": rune_1[0]["primaryStyle"],
                        "perkSubStyle": rune_1[0]["subStyle"],
                    }
                ),
                "positionPreference": position_1.upper(),   
                "skinId": 0,
                "spell1": summ_1[0],
                "spell2": summ_1[1],
            }

            body_2 = {
                "championId": championId_2,
                "perks": json.dumps(
                    {
                        "perkIds": [
                            rune_2[0]["primaryPerk1"],
                            rune_2[0]["primaryPerk2"],
                            rune_2[0]["primaryPerk3"],
                            rune_2[0]["primaryPerk4"],
                            rune_2[0]["subPerk1"],
                            rune_2[0]["subPerk2"],
                            rune_2[0]["offense"],
                            rune_2[0]["flex"],
                            rune_2[0]["defense"],
                        ],
                        "perkStyle": rune_2[0]["primaryStyle"],
                        "perkSubStyle": rune_2[0]["subStyle"],
                    }
                ),
                "positionPreference": position_2.upper(),   
                "skinId": 0,
                "spell1": summ_2[0],
                "spell2": summ_2[1],
            }

            await connection.request("put", "/lol-lobby/v1/lobby/members/localMember/player-slots", data=[body_1, body_2])

        if config.import_items:
            itemset_1 = create_itemset_body(
                championId_1,
                start_item_1,
                item_build_1,
                item_1,
                champion_name_1,
                boots_1,
            )

            itemset_2 = create_itemset_body(
                championId_2,
                start_item_2,
                item_build_2,
                item_2,
                champion_name_2,
                boots_2,
            )

            await set_itemset(
                itemsets=[itemset_1, itemset_2],
                connection=connection,
                accountId=accountId,
                summonerId=summonerId,
            )

        return


    except Exception as e:
        print("No Quick-Play builds found.")
        print(e)
        raise
        


async def set_rune_summ_item(connection, champion, position=""):
    if champion == None:
        return

    start = datetime.datetime.now()

    if position == "":
        localPlayerCellId = await get_localPlayerCellId(connection)
        if await is_aram(connection):
            position = "aram"
        else:
            position = await get_position(connection, localPlayerCellId)

    global rune, summ, skills

    (
        championId,
        rune,
        summ,
        item,
        start_item,
        item_build,
        skills,
        position,
        champion_name,
        boots,
    ) = client.get_build(champion, position, await get_summoner_name(connection))

    if isinstance(rune, dict):
        rune = [rune, rune, rune]

    print(champion_name)

    accountId, summonerId = await get_acc_sum_id(connection)

    if config.import_runes:
        await current_perks_delete(connection)
        await set_perks(connection, champion, rune[0], champion_name)

    if config.import_summs:
        await set_summs(connection, summ)

    if config.import_items:
        await set_itemset(
            connection,
            accountId,
            summonerId,
            champion,
            start_item,
            item_build,
            item,
            champion_name,
            boots,
        )

    print(datetime.datetime.now() - start)
    gui.set_info(
        championId, rune, summ, skills, position, item_build, start_item, boots, item
    )


def get_block(name):
    block = {
        "hideIfSummonerSpell": "",
        "items": [],
        "showIfSummonerSpell": "",
        "type": str(name),
    }
    return block

def create_itemset_body(
    champion,
    start_item,
    item_build,
    item,
    champion_name,
    boots,
):
    itemset_body = {
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
        "uid": "1",
    }

    id = 0
    for liste in start_item:
        itemset_body["blocks"].append(get_block("Start Items"))
        for i in liste:
            itemset_body["blocks"][id]["items"].append(
                {"count": 1, "id": str(i)}
            )
        id += 1

    itemset_body["blocks"].append(get_block("Boots"))
    for i in boots:
        itemset_body["blocks"][id]["items"].append({"count": 1, "id": str(i)})
    id += 1

    for liste in item_build:
        itemset_body["blocks"].append(get_block(("Build " + str(id - 3))))
        for i in liste:
            itemset_body["blocks"][id]["items"].append(
                {"count": 1, "id": str(i)}
            )
        id += 1

    itemset_body["blocks"].append(get_block("Items"))
    for i in item:
        itemset_body["blocks"][id]["items"].append({"count": 1, "id": str(i)})
    id += 1

    return itemset_body


async def set_itemset(
    connection,
    accountId,
    summonerId,
    champion=None,
    start_item=None,
    item_build=None,
    item=None,
    champion_name=None,
    boots=None,
    itemsets=None,
):
    body = {
        "accountId": accountId,
        "itemSets": [],
        "timestamp": 0,
    }

    if itemsets is not None:
        body["itemSets"] = itemsets
    else:
        itemset_body = create_itemset_body(
            champion, start_item, item_build, item, champion_name, boots
        )
        body["itemSets"].append(itemset_body)

    # print("summonerId:", summonerId)
    # print("body:", json.dumps(body, indent=4))

    await connection.request("put", "/lol-item-sets/v1/item-sets/" + str(summonerId) + "/sets", data=body)

    return


async def set_perks(connection, champion, rune, champion_name):
    body = {
        "name": champion_name,
        "primaryStyleId": rune["primaryStyle"],
        "subStyleId": rune["subStyle"],
        "selectedPerkIds": [
            rune["primaryPerk1"],
            rune["primaryPerk2"],
            rune["primaryPerk3"],
            rune["primaryPerk4"],
            rune["subPerk1"],
            rune["subPerk2"],
            rune["offense"],
            rune["flex"],
            rune["defense"],
        ],
        "quickPlayChampionIds": [champion],
        "current": True,
    }
    return await connection.request("post", "/lol-perks/v1/pages", data=body)


async def set_summs(connection, summ):
    if 4 in summ:
        if config.position_flash == 0 and summ[1] == 4:
            summ[1] = summ[0]
            summ[0] = 4
        elif config.position_flash == 1 and summ[0] == 4:
            summ[0] = summ[1]
            summ[1] = 4

    body = {"spell1Id": str(summ[0]), "spell2Id": str(summ[1])}
    return await connection.request(
        "patch", "/lol-champ-select/v1/session/my-selection", data=body
    )


async def current_perks_delete(connection):
    page = await connection.request("get", "/lol-perks/v1/currentpage")
    page = await page.content.read()
    print(page)
    try:
        if json.loads(page)["isTemporary"] == True:
            return await connection.request("delete", "/lol-perks/v1/pages")
        
        page_id = json.loads(page)["id"]
        print("page_id:", page_id)

        return await connection.request("delete", "/lol-perks/v1/pages/" + str(page_id))
    except:
        return await connection.request("delete", "/lol-perks/v1/pages")


async def get_acc_sum_id(connection):
    page = await connection.request(
        "get", "/lol-summoner/v1/current-summoner/account-and-summoner-ids"
    )
    page = await page.content.read()
    accountId = json.loads(page)["accountId"]
    summonerId = json.loads(page)["summonerId"]

    return accountId, summonerId


async def get_localPlayerCellId(connection):
    page = await connection.request("get", "/lol-champ-select/v1/session")
    page = await page.content.read()
    summoner = json.loads(page)
    return summoner["localPlayerCellId"]


async def get_position(connection, localPlayerCellId):
    page = await connection.request(
        "get", "/lol-champ-select/v1/summoners/" + str(localPlayerCellId)
    )
    page = await page.content.read()
    summoner = json.loads(page)
    return summoner["assignedPosition"]


async def is_aram(connection):
    page = await connection.request("get", "/lol-champ-select/v1/session")
    page = await page.content.read()
    page = json.loads(page)

    if (
        page["allowBattleBoost"] == True
        and page["allowRerolling"] == True
        and page["benchEnabled"] == True
    ):
        return True

    return False


async def get_summoner_name(connection):
    page = await connection.request("get", "/lol-summoner/v1/current-summoner")
    page = await page.content.read()
    summoner = json.loads(page)

    displayName = summoner["displayName"]
    gameName = summoner["gameName"]
    internalName = summoner["internalName"]
    summonerId = summoner["summonerId"]

    if displayName:
        summonerName = displayName
    elif gameName:
        summonerName = gameName
    elif internalName:
        summonerName = internalName
    else:
        summonerName = str(summonerId)
    
    return summonerName


def get_champion():
    return champion


def get_rune():
    return rune


def get_summ():
    return summ


def get_skills():
    return skills
