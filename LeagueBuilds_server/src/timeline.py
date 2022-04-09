
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
            if(event['type']=='SKILL_LEVEL_UP'):
                participants[event['participantId']]['SKILL_LEVEL_UP'].append(event)
                continue
            elif(event['type']=='ITEM_PURCHASED'):
                if(int(event['timestamp']) < 20000):
                    participants[event['participantId']]['START_ITEMS'].append(event)
                else:
                    participants[event['participantId']]['ITEMS'].append(event)
                continue
            elif(event['type']=='ITEM_UNDO'):
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

    return participants