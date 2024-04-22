from riotwatcher import LolWatcher, ApiError
from models.dynamics_db import SUMMONER, MATCHES, BUILDS, ARAM
import time, timeline, threading, queue
import api_key
from peewee import chunked
import logging, os

if (not os.path.exists('../../../log')):
    os.mkdir('../../../log')

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('../../../log/dynamics.log')
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

def clean_builds():
    logger.info('Clean Builds')
    BUILDS.delete().where(BUILDS.gameEndTimestamp < time.time()*1000 - 1250000000,).execute()
    ARAM.delete().where(ARAM.gameEndTimestamp < time.time()*1000 - 1250000000,).execute()
    logger.info('Builds cleaned')

def update_summoner():
    lol_watcher = LolWatcher(api_key.api_key)
    logger.info('Update Summoner')
    
    my_region = 'euw1'

    queue ='RANKED_SOLO_5x5'

    try:
        challenger = lol_watcher.league.challenger_by_queue(my_region, queue)
        grandmaster = lol_watcher.league.grandmaster_by_queue(my_region, queue)
        master = lol_watcher.league.masters_by_queue(my_region, queue)
    except ApiError as err:
        if err.response.status_code == 429:
            logger.warning(f'We should retry in {err.response.headers["Retry-After"]} seconds.')
        elif err.response.status_code == 404:
            logger.error('Summoner with that ridiculous name not found.')
        else:
            logger.debug(err)
            raise
        return

    data = challenger['entries'] + grandmaster['entries'] + master['entries']
    i=0

    summoner = []

    for item in data:
        if(not SUMMONER.get_or_none(SUMMONER.summonerId == item['summonerId'])):
            try:
                summ = lol_watcher.summoner.by_id(my_region, item['summonerId'])
            except ApiError as err:
                if err.response.status_code == 429:
                    logger.warning(f'We should retry in {err.response.headers["Retry-After"]} seconds.')
                elif err.response.status_code == 404:
                    logger.error('Summoner with that ridiculous name not found.')
                else:
                    logger.debug(err)
                    raise
                continue

            summoner.append({
                'summonerId' : item['summonerId'],
                'summonerName' : item['summonerName'],
                'puuid' : summ['puuid'],
            })

            logger.info(f'Summoner {str(i)}: {item["summonerName"]}')
        i+=1

        if len(summoner) >= 1000:
            for batch in chunked(summoner, 100):
                SUMMONER.insert_many(batch).on_conflict_replace().execute()
            summoner = []

    for batch in chunked(summoner, 100):
        SUMMONER.insert_many(batch).on_conflict_replace().execute()

def update_matches():
    lol_watcher = LolWatcher(api_key.api_key)
    logger.info('Update Matches')

    my_region = 'europe'

    summoners = SUMMONER.select()

    i = 0
    j = 0

    matches_list = []

    for summoner in summoners:
        try:
            matches = lol_watcher.match.matchlist_by_puuid(region=my_region, puuid=summoner.puuid, count=10, start=0, start_time=int(time.time() - 1250000))
        except ApiError as err:
            if err.response.status_code == 429:
                logger.warning(f'We should retry in {err.response.headers["Retry-After"]} seconds.')
            elif err.response.status_code == 404:
                logger.error('Summoner with that ridiculous name not found.')
            else:
                logger.debug(err)
                logger.warning(err)
            continue

        logger.info(f'Summoner {str(j)}: {summoner.summonerName}')

        if(len(matches) <= 0):
            logger.warning(f'Removed: {summoner.summonerName}')
            SUMMONER.delete().where(SUMMONER.summonerId == summoner.summonerId).execute()
            continue

        for match in matches:

            if(not BUILDS.get_or_none(BUILDS.matchId == match) or not ARAM.get_or_none(ARAM.matchId == match)):
                matches_list.append({
                    'matchId' : match,
                })

                logger.info(f'Match {str(i)}: {match}')
                i+=1
        
        j+=1

        if len(matches_list) >= 1000:
            for batch in chunked(matches_list, 100):
                MATCHES.insert_many(batch).on_conflict_replace().execute()
            matches_list = []

    for batch in chunked(matches_list, 100):
        MATCHES.insert_many(batch).on_conflict_replace().execute()

def update_builds():
    logger.info('Update Builds')

    matches = MATCHES.select()

    logger.info(f'Match count:\t{len(matches)}')

    logger.info('Fetched IDs')

    q = queue.Queue(maxsize=1000)
    num_threads = min(20, len(matches))

    repeat = False

    for match in matches:
        try:
            q.put((match.matchId,), block = False)
        except queue.Full:
            repeat = True
            break

    matches_delete = []
    builds_create = []
    aram_create = []

    for i in range(num_threads):
        worker = threading.Thread(target=build_worker, args=[q, matches_delete, builds_create, aram_create])
        worker.setDaemon(True)
        worker.start()

    logger.info('Workers started')

    try:
        while True:
            if q.unfinished_tasks > 0:
                time.sleep(1)
                logger.debug(q.unfinished_tasks)
            else:
                break
    except KeyboardInterrupt:
        raise

    time.sleep(5)
    
    MATCHES.delete().where(MATCHES.matchId << matches_delete).execute()

    logger.info('Matches deleted')

    for batch in chunked(builds_create, 100):
        BUILDS.insert_many(batch).on_conflict_replace().execute()

    for batch in chunked(aram_create, 100):
        ARAM.insert_many(batch).on_conflict_replace().execute()

    return repeat

def build_worker(q, matches_delete, builds_create, aram_create):
    lol_watcher = LolWatcher(api_key.api_key)
    my_region = 'europe'
    while not q.empty():
        work = q.get()
        match_id = work[0]
        q.task_done()

        try:
            match = lol_watcher.match.by_id(my_region, match_id)
        except ApiError as err:
            if err.response.status_code == 429:
                logger.warning(f'We should retry in {err.response.headers["Retry-After"]} seconds.')
                continue
            elif err.response.status_code == 404:
                logger.error('Summoner with that ridiculous name not found.')
                matches_delete.append(match_id)
                continue
            continue
        except:
            continue

        if(match['info']['gameEndTimestamp'] < time.time()*1000 - 1250000000):
            matches_delete.append(match_id)
            continue
            
        if(match['info']['gameType'] not in ['MATCHED_GAME'] or match['info']['gameMode'] not in ['CLASSIC', 'ARAM']):
            matches_delete.append(match_id)
            continue

        try:
            timeline_info = timeline.parse_timeline(lol_watcher, my_region, match_id)
        except ApiError as err:
            logger.debug(err)
            continue
        except:
            continue

        for participant in match['info']['participants']:
            if(match['info']['gameMode'] in ['CLASSIC']):
                builds_create.append({
                    'matchId' : match_id,
                    'gameEndTimestamp' : match['info']['gameEndTimestamp'],

                    'championId' : participant['championId'],
                    'championName' : participant['championName'],
                    'teamPosition' : participant['teamPosition'],
                    'individualPosition' : participant['individualPosition'],
                    'lane' : participant['lane'],

                    'item0' : participant['item0'],
                    'item1' : participant['item1'],
                    'item2' : participant['item2'],
                    'item3' : participant['item3'],
                    'item4' : participant['item4'],
                    'item5' : participant['item5'],
                    'item6' : participant['item6'],

                    'start_items' : timeline_info[participant['participantId']]['START_ITEMS'],
                    'items' : timeline_info[participant['participantId']]['ITEMS'],
                    'skills' : timeline_info[participant['participantId']]['SKILL_LEVEL_UP'],

                    'summoner1Id' : participant['summoner1Id'],
                    'summoner2Id' : participant['summoner2Id'],

                    'win' : participant['win'],

                    'defense' : participant['perks']['statPerks']['defense'],
                    'flex' : participant['perks']['statPerks']['flex'],
                    'offense' : participant['perks']['statPerks']['offense'],

                    'primaryStyle' : participant['perks']['styles'][0]['style'],
                    'primaryPerk1' : participant['perks']['styles'][0]['selections'][0]['perk'],
                    'primaryPerk2' : participant['perks']['styles'][0]['selections'][1]['perk'],
                    'primaryPerk3' : participant['perks']['styles'][0]['selections'][2]['perk'],
                    'primaryPerk4' : participant['perks']['styles'][0]['selections'][3]['perk'],

                    'subStyle' : participant['perks']['styles'][1]['style'],
                    'subPerk1' : participant['perks']['styles'][1]['selections'][0]['perk'],
                    'subPerk2' : participant['perks']['styles'][1]['selections'][1]['perk'],
                })
            else:
                aram_create.append({
                    'matchId' : match_id,
                    'gameEndTimestamp' : match['info']['gameEndTimestamp'],

                    'championId' : participant['championId'],
                    'championName' : participant['championName'],
                    'teamPosition' : participant['teamPosition'],
                    'individualPosition' : participant['individualPosition'],
                    'lane' : participant['lane'],

                    'item0' : participant['item0'],
                    'item1' : participant['item1'],
                    'item2' : participant['item2'],
                    'item3' : participant['item3'],
                    'item4' : participant['item4'],
                    'item5' : participant['item5'],
                    'item6' : participant['item6'],

                    'start_items' : timeline_info[participant['participantId']]['START_ITEMS'],
                    'items' : timeline_info[participant['participantId']]['ITEMS'],
                    'skills' : timeline_info[participant['participantId']]['SKILL_LEVEL_UP'],

                    'summoner1Id' : participant['summoner1Id'],
                    'summoner2Id' : participant['summoner2Id'],

                    'win' : participant['win'],

                    'defense' : participant['perks']['statPerks']['defense'],
                    'flex' : participant['perks']['statPerks']['flex'],
                    'offense' : participant['perks']['statPerks']['offense'],

                    'primaryStyle' : participant['perks']['styles'][0]['style'],
                    'primaryPerk1' : participant['perks']['styles'][0]['selections'][0]['perk'],
                    'primaryPerk2' : participant['perks']['styles'][0]['selections'][1]['perk'],
                    'primaryPerk3' : participant['perks']['styles'][0]['selections'][2]['perk'],
                    'primaryPerk4' : participant['perks']['styles'][0]['selections'][3]['perk'],

                    'subStyle' : participant['perks']['styles'][1]['style'],
                    'subPerk1' : participant['perks']['styles'][1]['selections'][0]['perk'],
                    'subPerk2' : participant['perks']['styles'][1]['selections'][1]['perk'],
                })

        logger.info(f'Match: {match_id}')
        matches_delete.append(match_id)