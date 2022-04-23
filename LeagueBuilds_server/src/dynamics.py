from riotwatcher import LolWatcher, ApiError
from models.dynamics_db import SUMMONER, MATCHES, BUILDS
import time, timeline, threading, queue
import config

def clean_builds():
    print('Clean Builds')
    BUILDS.delete().where(BUILDS.gameEndTimestamp < time.time()*1000 - 1250000000,).execute()
    print('Builds cleaned')

def update_summoner():
    lol_watcher = LolWatcher(config.api_key)
    print('Update Summoner')
    
    my_region = 'euw1'

    queue ='RANKED_SOLO_5x5'

    try:
        challenger = lol_watcher.league.challenger_by_queue(my_region, queue)
        grandmaster = lol_watcher.league.grandmaster_by_queue(my_region, queue)
        master = lol_watcher.league.masters_by_queue(my_region, queue)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            print(err)
            raise
        return

    data = challenger['entries'] + grandmaster['entries'] + master['entries']
    i=0

    for item in data:
        if(not SUMMONER.get_or_none(SUMMONER.summonerId == item['summonerId'])):
            summ = lol_watcher.summoner.by_id(my_region, item['summonerId'])
            SUMMONER.create(
                summonerId = item['summonerId'],
                summonerName = item['summonerName'],
                puuid = summ['puuid'],
            )
            print("Summoner " + str(i) + ": " + item['summonerName'])
        i+=1

def update_matches():
    lol_watcher = LolWatcher(config.api_key)
    print('Update Matches')

    my_region = 'europe'

    summoners = SUMMONER.select()

    i = 0
    j = 0

    for summoner in summoners:
        try:
            matches = lol_watcher.match.matchlist_by_puuid(region=my_region, puuid=summoner.puuid, count=10, start=0)
        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            elif err.response.status_code == 404:
                print('Summoner with that ridiculous name not found.')
            else:
                print(err)
                raise
            continue

        print("Summoner " + str(j) + ": " + summoner.summonerName)

        for match in matches:

            if(not BUILDS.get_or_none(BUILDS.matchId == match)):
                MATCHES.replace(
                    matchId = match,
                ).execute()
                print("Match " + str(i) + ": " + match)
                i+=1
        
        j+=1

def update_builds():
    print('Update Builds')

    matches = MATCHES.select()

    print('Fetched IDs')

    q = queue.Queue(maxsize=0)
    num_threads = min(20, len(matches))

    for match in matches:
        q.put((match.matchId,))

    matches_delete = []

    for i in range(num_threads):
        worker = threading.Thread(target=build_worker, args=[q, matches_delete])
        worker.setDaemon(True)
        worker.start()

    print('Workers started')

    try:
        while True:
            if q.unfinished_tasks > 0:
                time.sleep(1)
                print(q.unfinished_tasks)
            else:
                break
    except KeyboardInterrupt:
        raise

    time.sleep(5)
    
    MATCHES.delete().where(MATCHES.matchId in matches_delete).execute()

    print('Matches deleted')

def build_worker(q, matches_delete):
    lol_watcher = LolWatcher(config.api_key)
    my_region = 'europe'
    while not q.empty():
        work = q.get()
        match_id = work[0]
        q.task_done()

        try:
            match = lol_watcher.match.by_id(my_region, match_id)
        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
                continue
            elif err.response.status_code == 404:
                print('Summoner with that ridiculous name not found.')
                matches_delete.append(match_id)
                continue
        except:
            continue

        if(match['info']['gameEndTimestamp'] < time.time()*1000 - 1250000000):
            matches_delete.append(match_id)
            continue
            
        if(match['info']['gameType'] not in ['MATCHED_GAME'] or match['info']['gameMode'] not in ['CLASSIC']):
            matches_delete.append(match_id)
            continue

        try:
            timeline_info = timeline.parse_timeline(lol_watcher, my_region, match_id)
        except ApiError as err:
            print(err)
            continue
        except:
            continue

        for participant in match['info']['participants']:
            while True:
                try:
                    BUILDS.replace(
                        matchId = match_id,
                        gameEndTimestamp = match['info']['gameEndTimestamp'],

                        championId = participant['championId'],
                        championName = participant['championName'],
                        teamPosition = participant['teamPosition'],
                        individualPosition = participant['individualPosition'],
                        lane = participant['lane'],

                        item0 = participant['item0'],
                        item1 = participant['item1'],
                        item2 = participant['item2'],
                        item3 = participant['item3'],
                        item4 = participant['item4'],
                        item5 = participant['item5'],
                        item6 = participant['item6'],

                        start_items = timeline_info[participant['participantId']]['START_ITEMS'],
                        items = timeline_info[participant['participantId']]['ITEMS'],
                        skills = timeline_info[participant['participantId']]['SKILL_LEVEL_UP'],

                        summoner1Id = participant['summoner1Id'],
                        summoner2Id = participant['summoner2Id'],

                        win = participant['win'],

                        defense = participant['perks']['statPerks']['defense'],
                        flex = participant['perks']['statPerks']['flex'],
                        offense = participant['perks']['statPerks']['offense'],

                        primaryStyle = participant['perks']['styles'][0]['style'],
                        primaryPerk1 = participant['perks']['styles'][0]['selections'][0]['perk'],
                        primaryPerk2 = participant['perks']['styles'][0]['selections'][1]['perk'],
                        primaryPerk3 = participant['perks']['styles'][0]['selections'][2]['perk'],
                        primaryPerk4 = participant['perks']['styles'][0]['selections'][3]['perk'],

                        subStyle = participant['perks']['styles'][1]['style'],
                        subPerk1 = participant['perks']['styles'][1]['selections'][0]['perk'],
                        subPerk2 = participant['perks']['styles'][1]['selections'][1]['perk'],
                    ).execute()
                except:
                    print('locked')
                    continue
                break

        print("Match: " + match_id)
        matches_delete.append(match_id)