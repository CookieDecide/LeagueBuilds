from riotwatcher import LolWatcher, ApiError
from models.dynamics_db import SUMMONER, MATCHES, BUILDS
import time, timeline
import config

lol_watcher = LolWatcher(config.api_key)

def clean_builds():
    builds = BUILDS.select().where(BUILDS.gameEndTimestamp < time.time()*1000 - 1250000000,)
    
    for build in builds:
        if(build.gameEndTimestamp):
            if(int(build.gameEndTimestamp) < time.time()*1000 - 1250000000):
                print("Removed: " + build.matchId)
                build.delete_instance()
        else:
            print("Removed: " + build.matchId)
            build.delete_instance()

def update_summoner():
    try:
        my_region = 'euw1'

        queue ='RANKED_SOLO_5x5'

        challenger = lol_watcher.league.challenger_by_queue(my_region, queue)
        grandmaster = lol_watcher.league.grandmaster_by_queue(my_region, queue)
        master = lol_watcher.league.masters_by_queue(my_region, queue)

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
                time.sleep(1.2)
            i+=1



        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            print(err)
            raise

def update_matches():
    try:
        my_region = 'europe'

        summoners = SUMMONER.select()

        i = 0
        j = 0

        for summoner in summoners:
            matches = lol_watcher.match.matchlist_by_puuid(region=my_region, puuid=summoner.puuid, count=10, start=0)
            print("Summoner " + str(j) + ": " + summoner.summonerName)

            for match in matches:

                if(not MATCHES.get_or_none(MATCHES.matchId == match)):
                    MATCHES.create(
                        matchId = match,
                    )
                    print("Match " + str(i) + ": " + match)
                    i+=1
            
            j+=1
            time.sleep(1.2)



        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            print(err)
            raise

def update_builds():
    try:
        my_region = 'europe'

        matches = MATCHES.select()
        builds = BUILDS.select(BUILDS.matchId).distinct()
        build_ids = []
        match_ids = []
        for build in builds:
            build_ids.append(build.matchId)
        for match in matches:
            match_ids.append(match.matchId)
            
        matches = list(set(match_ids) - set(build_ids))

        i = 0

        for match_id in matches:
            try:
                match = lol_watcher.match.by_id(my_region, match_id)
            except ApiError as err:
                print(err)
                time.sleep(0.6)
                if err.response.status_code == 404:
                    print('Match with that ridiculous name not found.')
                    MATCHES.get(MATCHES.matchId == match_id).delete_instance()
                    continue
            if(match['info']['gameEndTimestamp'] < time.time()*1000 - 1250000000):
                MATCHES.get(MATCHES.matchId == match_id).delete_instance()
                time.sleep(0.6)
                i+=1
                continue
                
            if(match['info']['gameType'] not in ['MATCHED_GAME'] or match['info']['gameMode'] not in ['CLASSIC']):
                MATCHES.get(MATCHES.matchId == match_id).delete_instance()
                time.sleep(0.6)
                i+=1
                continue

            try:
                time.sleep(0.6)
                timeline_info = timeline.parse_timeline(lol_watcher, my_region, match_id)
            except ApiError as err:
                print(err)
                time.sleep(0.6)
                continue
            for participant in match['info']['participants']:
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

            print("Match " + str(i) + ": " + match_id)
            time.sleep(0.6)
                
            i+=1



        
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            print(err)
            raise