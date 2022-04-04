
def parse_timeline(lol_watcher, my_region, matchId):
    participants = {
        1: {"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
        2: {"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
        3: {"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
        4: {"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
        5: {"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
        6: {"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
        7: {"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
        8: {"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
        9: {"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
        10:{"SKILL_LEVEL_UP": [], "START_ITEMS": [], "ITEMS": [],},
    }

    timeline = lol_watcher.match.timeline_by_match(my_region, matchId)

    for frame in timeline['info']['frames']:
        for event in frame['events']:
            if(event['type']=='OBJECTIVE_BOUNTY_PRESTART'):
                '''
                "actualStartTime": 855000,
                "teamId": 200,
                "timestamp": 840284,
                "type": "OBJECTIVE_BOUNTY_PRESTART"
                '''
                continue
            elif(event['type']=='SKILL_LEVEL_UP'):
                '''
                "levelUpType": "NORMAL",
                "participantId": 7,
                "skillSlot": 1,
                "timestamp": 18782,
                "type": "SKILL_LEVEL_UP"
                '''
                participants[event['participantId']]['SKILL_LEVEL_UP'].append(event)
                continue
            elif(event['type']=='ITEM_DESTROYED'):
                '''
                "itemId": 3340,
                "participantId": 5,
                "timestamp": 44997,
                "type": "ITEM_DESTROYED"
                '''
                continue
            elif(event['type']=='WARD_KILL'):
                '''
                "killerId": 7,
                "timestamp": 923846,
                "type": "WARD_KILL",
                "wardType": "SIGHT_WARD"
                "wardType": "UNDEFINED"
                "wardType": "BLUE_TRINKET"
                "wardType": "CONTROL_WARD"
                "wardType": "YELLOW_TRINKET"
                '''
                continue
            elif(event['type']=='BUILDING_KILL'):
                '''
                "assistingParticipantIds": [
                    5
                ],
                "bounty": 0,
                "buildingType": "TOWER_BUILDING",
                "buildingType": "INHIBITOR_BUILDING",
                "killerId": 4,
                "laneType": "BOT_LANE",
                "position": {
                    "x": 13866,
                    "y": 4505
                },
                "teamId": 200,
                "timestamp": 767712,
                "towerType": "OUTER_TURRET",
                "towerType": "INNER_TURRET",
                "towerType": "BASE_TURRET",
                "towerType": "NEXUS_TURRET",
                "type": "BUILDING_KILL"
                '''
                continue
            elif(event['type']=='LEVEL_UP'):
                '''
                "level": 2,
                "participantId": 7,
                "timestamp": 105655,
                "type": "LEVEL_UP"
                '''
                continue
            elif(event['type']=='ITEM_PURCHASED'):
                '''
                "itemId": 3862,
                "participantId": 5,
                "timestamp": 2035,
                "type": "ITEM_PURCHASED"
                '''
                if(int(event['timestamp']) < 20000):
                    participants[event['participantId']]['START_ITEMS'].append(event)
                else:
                    participants[event['participantId']]['ITEMS'].append(event)
                continue
            elif(event['type']=='TURRET_PLATE_DESTROYED'):
                '''
                "killerId": 0,
                "laneType": "TOP_LANE",
                "position": {
                    "x": 4318,
                    "y": 13875
                },
                "teamId": 200,
                "timestamp": 399687,
                "type": "TURRET_PLATE_DESTROYED"
                '''
                continue
            elif(event['type']=='CHAMPION_KILL'):
                '''
                "assistingParticipantIds": [
                    4
                ],
                "bounty": 274,
                "killStreakLength": 1,
                "killerId": 5,
                "position": {
                    "x": 13122,
                    "y": 2463
                },
                "shutdownBounty": 0,
                "timestamp": 797244,
                "type": "CHAMPION_KILL",
                "victimDamageDealt": [
                    {
                        "basic": true,
                        "magicDamage": 0,
                        "name": "Xayah",
                        "participantId": 4,
                        "physicalDamage": 90,
                        "spellName": "xayahpassive",
                        "spellSlot": 63,
                        "trueDamage": 0,
                        "type": "OTHER"
                    },
                    {
                        "basic": false,
                        "magicDamage": 0,
                        "name": "Xayah",
                        "participantId": 4,
                        "physicalDamage": 18,
                        "spellName": "xayahw",
                        "spellSlot": 1,
                        "trueDamage": 0,
                        "type": "OTHER"
                    }
                ],
                "victimDamageReceived": [
                    {
                        "basic": false,
                        "magicDamage": 139,
                        "name": "MissFortune",
                        "participantId": 4,
                        "physicalDamage": 0,
                        "spellName": "missfortunescattershot",
                        "spellSlot": 2,
                        "trueDamage": 0,
                        "type": "OTHER"
                    },
                    {
                        "basic": true,
                        "magicDamage": 0,
                        "name": "MissFortune",
                        "participantId": 4,
                        "physicalDamage": 91,
                        "spellName": "missfortunebasicattack",
                        "spellSlot": 64,
                        "trueDamage": 0,
                        "type": "OTHER"
                    },
                    {
                        "basic": false,
                        "magicDamage": 17,
                        "name": "MissFortune",
                        "participantId": 4,
                        "physicalDamage": 56,
                        "spellName": "",
                        "spellSlot": -1,
                        "trueDamage": 0,
                        "type": "OTHER"
                    },
                    {
                        "basic": true,
                        "magicDamage": 0,
                        "name": "MissFortune",
                        "participantId": 4,
                        "physicalDamage": 91,
                        "spellName": "missfortunepassive",
                        "spellSlot": 63,
                        "trueDamage": 0,
                        "type": "OTHER"
                    },
                    {
                        "basic": false,
                        "magicDamage": 0,
                        "name": "MissFortune",
                        "participantId": 4,
                        "physicalDamage": 63,
                        "spellName": "missfortunepassive",
                        "spellSlot": 63,
                        "trueDamage": 0,
                        "type": "OTHER"
                    },
                    {
                        "basic": true,
                        "magicDamage": 0,
                        "name": "SRU_OrderMinionSiege",
                        "participantId": 0,
                        "physicalDamage": 44,
                        "spellName": "sru_orderminionrangedbasicattack",
                        "spellSlot": 64,
                        "trueDamage": 0,
                        "type": "MINION"
                    },
                    {
                        "basic": true,
                        "magicDamage": 0,
                        "name": "SRU_OrderMinionSiege",
                        "participantId": 0,
                        "physicalDamage": 70,
                        "spellName": "sru_orderminionsiegebasicattack",
                        "spellSlot": 64,
                        "trueDamage": 0,
                        "type": "MINION"
                    },
                    {
                        "basic": true,
                        "magicDamage": 0,
                        "name": "SRU_OrderMinionSiege",
                        "participantId": 0,
                        "physicalDamage": 59,
                        "spellName": "sru_orderminionrangedbasicattack2",
                        "spellSlot": 65,
                        "trueDamage": 0,
                        "type": "MINION"
                    },
                    {
                        "basic": false,
                        "magicDamage": 0,
                        "name": "Senna",
                        "participantId": 5,
                        "physicalDamage": 60,
                        "spellName": "sennapassive",
                        "spellSlot": 63,
                        "trueDamage": 0,
                        "type": "OTHER"
                    },
                    {
                        "basic": true,
                        "magicDamage": 0,
                        "name": "Senna",
                        "participantId": 5,
                        "physicalDamage": 112,
                        "spellName": "sennabasicattack2",
                        "spellSlot": 65,
                        "trueDamage": 0,
                        "type": "OTHER"
                    },
                    {
                        "basic": false,
                        "magicDamage": 0,
                        "name": "Senna",
                        "participantId": 5,
                        "physicalDamage": 140,
                        "spellName": "sennaw",
                        "spellSlot": 1,
                        "trueDamage": 0,
                        "type": "OTHER"
                    },
                    {
                        "basic": true,
                        "magicDamage": 0,
                        "name": "Senna",
                        "participantId": 5,
                        "physicalDamage": 177,
                        "spellName": "sennacritattack",
                        "spellSlot": 73,
                        "trueDamage": 0,
                        "type": "OTHER"
                    }
                ],
                "victimId": 9
                '''
                continue
            elif(event['type']=='PAUSE_END'):
                '''
                "realTimestamp": 1648934128608,
                "timestamp": 0,
                "type": "PAUSE_END"
                '''
                continue
            elif(event['type']=='ITEM_UNDO'):
                '''
                "afterId": 0,
                "beforeId": 1053,
                "goldGain": 900,
                "participantId": 5,
                "timestamp": 549125,
                "type": "ITEM_UNDO"
                '''
                '''
                "itemId": 3862,
                "participantId": 5,
                "timestamp": 2035,
                "type": "ITEM_PURCHASED"
                '''
                if(int(event['afterId']) == 0):
                    if(int(event['timestamp']) < 20000):
                        participants[event['participantId']]['START_ITEMS'].pop()
                    else:
                        try:
                            participants[event['participantId']]['ITEMS'].pop()
                        except:
                            participants[event['participantId']]['START_ITEMS'].pop()
                else:
                    if(int(event['timestamp']) < 20000):
                        participants[event['participantId']]['START_ITEMS'].append({"itemId": event['afterId'], "participantId": event['participantId'], "timestamp": event['timestamp'], "type": "ITEM_PURCHASED"})
                    else:
                        participants[event['participantId']]['ITEMS'].append({"itemId": event['afterId'], "participantId": event['participantId'], "timestamp": event['timestamp'], "type": "ITEM_PURCHASED"})
                continue
            elif(event['type']=='WARD_PLACED'):
                '''
                "creatorId": 5,
                "timestamp": 43494,
                "type": "WARD_PLACED",
                "wardType": "YELLOW_TRINKET"
                "wardType": "UNDEFINED"
                "wardType": "CONTROL_WARD"
                "wardType": "SIGHT_WARD"
                "wardType": "BLUE_TRINKET"
                '''
                continue
            elif(event['type']=='CHAMPION_SPECIAL_KILL'):
                '''
                "killType": "KILL_FIRST_BLOOD",
                "killType": "KILL_MULTI",
                "multiKillLength": 2,
                "killerId": 1,
                "position": {
                    "x": 6946,
                    "y": 8273
                },
                "timestamp": 369374,
                "type": "CHAMPION_SPECIAL_KILL"
                '''
                continue
            elif(event['type']=='ELITE_MONSTER_KILL'):
                '''
                "assistingParticipantIds": [
                    5
                ],
                "bounty": 0,
                "killerId": 7,
                "killerTeamId": 200,
                "monsterType": "RIFTHERALD",
                "monsterType": "BARON_NASHOR",
                "monsterSubType": "AIR_DRAGON",
                "monsterSubType": "HEXTECH_DRAGON",
                "monsterSubType": "WATER_DRAGON",
                "monsterSubType": "FIRE_DRAGON",
                "monsterSubType": "EARTH_DRAGON",
                "monsterType": "DRAGON",
                "position": {
                    "x": 5346,
                    "y": 10650
                },
                "timestamp": 545813,
                "type": "ELITE_MONSTER_KILL"
                '''
                continue
            elif(event['type']=='ITEM_SOLD'):
                '''
                "itemId": 2010,
                "participantId": 10,
                "timestamp": 660284,
                "type": "ITEM_SOLD"
                '''
                continue
            elif(event['type']=='GAME_END'):
                '''
                "gameId": 5795347656,
                "realTimestamp": 1648338270587,
                "timestamp": 1091781,
                "type": "GAME_END",
                "winningTeam": 100
                '''
                continue
            elif(event['type']=='DRAGON_SOUL_GIVEN'):
                '''
                "name": "Mountain",
                "name": "Hextech",
                "name": "Cloud",
                "name": "Infernal",
                "name": "Ocean",
                "teamId": 100,
                "timestamp": 1719250,
                "type": "DRAGON_SOUL_GIVEN"
                '''
                continue
            elif(event['type']=='OBJECTIVE_BOUNTY_FINISH'):
                '''
                "teamId": 200,
                "timestamp": 1114537,
                "type": "OBJECTIVE_BOUNTY_FINISH"
                '''
                continue
            elif(event['type']=='CHAMPION_TRANSFORM'):
                '''
                'participantId': 2, 
                'timestamp': 762152, 
                'transformType': 'SLAYER', 
                'type': 'CHAMPION_TRANSFORM'
                '''
                continue
            else:
                print('ERROR TYPE NOT DOCUMENTED!')
                print(event)

    return participants