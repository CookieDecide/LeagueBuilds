import numpy, json, ast
from models.statics_db import ITEMS, CHAMPIONS
from models.dynamics_db import BUILDS, ARAM
from models.builds_db import FINALBUILDS
import time, datetime, queue, threading
from peewee import chunked
from joblib import Parallel, delayed, effective_n_jobs
import logging, os

class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level

if (not os.path.exists('../../../log')):
    os.mkdir('../../../log')

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('../../../log/sorting.log')
debug_handler = logging.FileHandler('../../../log/debug.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)
debug_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
debug_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
debug_handler.setFormatter(debug_format)

# Set Filters
debug_handler.addFilter(MyFilter(logging.DEBUG))

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.addHandler(debug_handler)

def init():
    logger.info('Initialize Items')
    items_all = ITEMS.select()

    valid_items, valid_start_items, valid_boots = [], [], []

    for item in items_all:
        if('Trinket' not in item.tags):
            valid_start_items.append(int(item.id))
            if((int(item.depth) == 3 or item.into == '0') and '1001' not in item.from_ and 'Consumable' not in item.tags and 'GoldPer' not in item.tags and 'Jungle' not in item.tags):
                valid_items.append(int(item.id))
            if('1001' in item.from_):
                valid_boots.append(int(item.id))
    logger.info('Initialize Items finished')

    return valid_items, valid_start_items, valid_boots

def get_builds(champion, position):
    if(position==''):
        builds = BUILDS.select(
            BUILDS.championId,
            BUILDS.championName,
            BUILDS.teamPosition,

            BUILDS.item0,
            BUILDS.item1,
            BUILDS.item2,
            BUILDS.item3,
            BUILDS.item4,
            BUILDS.item5,
            BUILDS.item6,

            BUILDS.start_items,
            BUILDS.items,
            BUILDS.skills,

            BUILDS.summoner1Id,
            BUILDS.summoner2Id,

            BUILDS.defense,
            BUILDS.flex,
            BUILDS.offense,

            BUILDS.primaryStyle,
            BUILDS.primaryPerk1,
            BUILDS.primaryPerk2,
            BUILDS.primaryPerk3,
            BUILDS.primaryPerk4,

            BUILDS.subStyle,
            BUILDS.subPerk1,
            BUILDS.subPerk2,
        ).where(
            BUILDS.championId == str(champion),
            BUILDS.teamPosition != "",
            #BUILDS.gameEndTimestamp >= time.time()*1000 - 1250000000,
        ).dicts()
    else:
        builds = BUILDS.select(
            BUILDS.championId,
            BUILDS.championName,
            BUILDS.teamPosition,

            BUILDS.item0,
            BUILDS.item1,
            BUILDS.item2,
            BUILDS.item3,
            BUILDS.item4,
            BUILDS.item5,
            BUILDS.item6,
            
            BUILDS.start_items,
            BUILDS.items,
            BUILDS.skills,

            BUILDS.summoner1Id,
            BUILDS.summoner2Id,

            BUILDS.defense,
            BUILDS.flex,
            BUILDS.offense,

            BUILDS.primaryStyle,
            BUILDS.primaryPerk1,
            BUILDS.primaryPerk2,
            BUILDS.primaryPerk3,
            BUILDS.primaryPerk4,

            BUILDS.subStyle,
            BUILDS.subPerk1,
            BUILDS.subPerk2,
        ).where(
            BUILDS.championId == str(champion),
            BUILDS.teamPosition == str(position).upper(),
            #BUILDS.gameEndTimestamp >= time.time()*1000 - 1250000000,
        ).dicts()

    return list(builds)

def get_aram(champion):
    builds = ARAM.select(
        ARAM.championId,
        ARAM.championName,
        ARAM.teamPosition,

        ARAM.item0,
        ARAM.item1,
        ARAM.item2,
        ARAM.item3,
        ARAM.item4,
        ARAM.item5,
        ARAM.item6,
        
        ARAM.start_items,
        ARAM.items,
        ARAM.skills,

        ARAM.summoner1Id,
        ARAM.summoner2Id,

        ARAM.defense,
        ARAM.flex,
        ARAM.offense,

        ARAM.primaryStyle,
        ARAM.primaryPerk1,
        ARAM.primaryPerk2,
        ARAM.primaryPerk3,
        ARAM.primaryPerk4,

        ARAM.subStyle,
        ARAM.subPerk1,
        ARAM.subPerk2,
    ).where(
        ARAM.championId == str(champion),
        #ARAM.gameEndTimestamp >= time.time()*1000 - 1250000000,
    ).dicts()

    return list(builds)

def info(champion, position, valid_items, valid_start_items, valid_boots):
    if (position == 'aram'):
        builds = get_aram(champion)
    else:
        builds = get_builds(champion, position)

    runes = []
    summs = []
    stats = []
    items = []
    start_items = []
    items_build = []
    skills = []
    boots = []
    
    for build in builds:
        runes.append(json.dumps({"primaryStyle": build['primaryStyle'],
                                "primaryPerk1": build['primaryPerk1'],
                                "primaryPerk2": build['primaryPerk2'],
                                "primaryPerk3": build['primaryPerk3'],
                                "primaryPerk4": build['primaryPerk4'],
                                "subStyle": build['subStyle'],
                                "subPerk1": build['subPerk1'],
                                "subPerk2": build['subPerk2']}))

        summs.append(build['summoner1Id'])
        summs.append(build['summoner2Id'])

        stats.append(json.dumps({"defense": build['defense'],
                                "flex": build['flex'],
                                "offense": build['offense']}))

        if(build['item0'] in valid_items):
            items.append(build['item0'])
        if(build['item1'] in valid_items):
            items.append(build['item1'])
        if(build['item2'] in valid_items):
            items.append(build['item2'])
        if(build['item3'] in valid_items):
            items.append(build['item3'])
        if(build['item4'] in valid_items):
            items.append(build['item4'])
        if(build['item5'] in valid_items):
            items.append(build['item5'])

        start_item_list = []
        for item in ast.literal_eval(build['start_items']):
            if(item['itemId'] in valid_start_items):
                start_item_list.append(item['itemId'])
        if(start_item_list):
            start_items.append(json.dumps(start_item_list))

        items_build_list = []
        boots_list = []
        for item in ast.literal_eval(build['items']):
            if(item['itemId'] in valid_items):
                items_build_list.append(item['itemId'])
            elif (item['itemId'] in valid_boots):
                boots_list.append(item['itemId'])
        if(items_build_list and len(items_build_list)>2):
            items_build.append(json.dumps(items_build_list[0:3]))
        if(boots_list and len(boots_list)>0):
            boots.append(json.dumps(boots_list[0]))

        skills_list = []
        for skill in ast.literal_eval(build['skills']):
            skills_list.append(skill['skillSlot'])
        if(skills_list and len(skills_list)>7):
            skills.append(json.dumps(skills_list[0:8]))

    for item in items:
        if(int(item) not in valid_items):
            items.remove(item)

    rune = sort_runes(runes)

    summ = sort_summs(summs)

    stat = sort_stats(stats)

    item = sort_items(items)

    start_item = sort_start_items(start_items)

    item_build = sort_items_build(items_build)

    skill_order = sort_skills(skills)

    boot = sort_boots(boots)

    return (rune|stat, summ, item, start_item, item_build, skill_order, boot)

def sort_runes(runes):
    rune, rune_count = numpy.unique(runes, return_counts=True)

    #if (len(rune)==0):
    #    return []

    return json.loads(rune[rune_count.tolist().index(max(rune_count))])

def sort_summs(summs):
    summ, summ_count = numpy.unique(summs, return_counts=True)
    summ_count_sort_ind = numpy.argsort(-summ_count)

    #if (len(summ)==0):
    #    return []

    return summ[summ_count_sort_ind][0:2].tolist()

def sort_stats(stats):
    stat, stat_count = numpy.unique(stats, return_counts=True)

    #if (len(stat)==0):
    #    return []

    return json.loads(stat[stat_count.tolist().index(max(stat_count))])

def sort_items(items):
    item, item_count = numpy.unique(items, return_counts=True)
    item_count_sort_ind = numpy.argsort(-item_count)
    sorted_items = []

    #if (len(item)==0):
    #    return []

    for i in item[item_count_sort_ind].tolist():
        sorted_items.append(int(i))

    return sorted_items

def sort_start_items(start_items):
    start_item, start_item_count = numpy.unique(start_items, return_counts=True)
    start_item_count_sort_ind = numpy.argsort(-start_item_count)

    #if (len(start_item)==0):
    #    return []

    if (len(start_item[start_item_count_sort_ind])<3):
        return [json.loads(start_item[start_item_count_sort_ind][0])]
    else:
        return [json.loads(start_item[start_item_count_sort_ind][0]), json.loads(start_item[start_item_count_sort_ind][1]), json.loads(start_item[start_item_count_sort_ind][2])]

def sort_items_build(items_build):
    item_build, item_build_count = numpy.unique(items_build, return_counts=True)
    item_build_count_sort_ind = numpy.argsort(-item_build_count)

    #if (len(item_build)==0):
    #    return []

    if (len(item_build[item_build_count_sort_ind])<3):
        return [json.loads(item_build[item_build_count_sort_ind][0])]
    else:
        return [json.loads(item_build[item_build_count_sort_ind][0]), json.loads(item_build[item_build_count_sort_ind][1]), json.loads(item_build[item_build_count_sort_ind][2])]

def sort_skills(skills):
    skill, skill_count = numpy.unique(skills, return_counts=True)
    skill_count_sort_ind = numpy.argsort(-skill_count)

    #if (len(skill)==0):
    #    return []

    return json.loads(skill[skill_count_sort_ind][0])

def sort_boots(boots):
    boot, boot_count = numpy.unique(boots, return_counts=True)
    boot_count_sort_ind = numpy.argsort(-boot_count)

    # Cassiopeia fix
    if (len(boot)==0):
        return []

    if (len(boot[boot_count_sort_ind])<3):
        return [json.loads(boot[boot_count_sort_ind][0])]
    else:
        return [json.loads(boot[boot_count_sort_ind][0]), json.loads(boot[boot_count_sort_ind][1]), json.loads(boot[boot_count_sort_ind][2])]

'''

def sort_all():
    start = datetime.datetime.now()
    champion_query = CHAMPIONS.select()
    for champion in champion_query:
        print(champion.champion)
        for position in ['', 'top', 'bottom', 'jungle', 'utility', 'middle', 'aram']:
            try:
                rune,summ,item,start_item,item_build,skills,boots = info(champion.key, position)
            except:
                continue

            FINALBUILDS.replace(
                championId = champion.key,
                runes = rune,
                summ = summ,
                item = item,
                start_item = start_item,
                item_build = item_build,
                skill_order = skills,
                position = position,
                boots = boots,
            ).execute()
    print(datetime.datetime.now() - start)

def sort_all_parallel():
    start = datetime.datetime.now()
    champion_query = CHAMPIONS.select()

    q = queue.Queue(maxsize=2000)
    num_threads = min(100, len(champion_query) * 7)

    for champion in champion_query:
        for position in ['', 'top', 'bottom', 'jungle', 'utility', 'middle', 'aram']:
            try:
                q.put((champion, position,), block = False)
            except queue.Full:
                print('Full!')
                break

    final_builds = []

    print('Starting Workers')

    for i in range(num_threads):
        worker = threading.Thread(target=sort_worker, args=[i, q, final_builds])
        worker.daemon = True
        worker.start()

    print('Workers started')

    try:
        while True:
            if q.unfinished_tasks > 0:
                time.sleep(1)
                print("Left to sort: ", q.unfinished_tasks)
            else:
                break
    except KeyboardInterrupt:
        raise

    time.sleep(5)

    for batch in chunked(final_builds, 100):
        FINALBUILDS.insert_many(batch).on_conflict_replace().execute()

    final_builds = []

    print('Finished in: ', datetime.datetime.now() - start)



def sort_worker(worker_id, q, final_builds):

    while not q.empty():
        start = time.time()

        work = q.get()
        champion = work[0]
        position = work[1]
        
        try:
            rune,summ,item,start_item,item_build,skills,boots = info(champion.key, position)
        except Exception as e:
            print(worker_id, '\tChampion: ', champion, '\tPosition: ', position, '\t', time.time() - start, '\tFAILED!')
            print(e)
            q.task_done()
            continue

        final_builds.append({
            'championId' : champion.key,
            'runes' : rune,
            'summ' : summ,
            'item' : item,
            'start_item' : start_item,
            'item_build' : item_build,
            'skill_order' : skills,
            'position' : position,
            'boots' : boots,
        })

        q.task_done()
        print(worker_id, '\tChampion: ', champion, '\tPosition: ', position, '\t', time.time() - start)

'''

def sort_pro():
    logger.info("Sorting started")
    start = time.time()
    champion_query = CHAMPIONS.select()

    valid_items, valid_start_items, valid_boots = init()
    njobs = effective_n_jobs()
    logger.info(f'effective_n_jobs: {njobs}')
    Parallel(n_jobs=njobs, backend="loky")(delayed(pro_worker)(champion, valid_items, valid_start_items, valid_boots) for champion in champion_query)

    logger.info(f'Sorting finished in: {time.time() - start}')

def pro_worker(champion, valid_items, valid_start_items, valid_boots):
    logger.info(f'Sorting started for:\t{champion}\t{os.getpid()}')

    for position in ['', 'top', 'bottom', 'jungle', 'utility', 'middle', 'aram']:
        start = time.time()

        try:
            rune,summ,item,start_item,item_build,skills,boots = info(champion.key, position, valid_items, valid_start_items, valid_boots)
        except Exception as e:
            logger.info(f'Champion: {champion}\tPosition: {position}\t{time.time() - start}\tFAILED!')
            logger.error(e)
            continue

        FINALBUILDS.replace(
            championId = champion.key,
            runes = rune,
            summ = summ,
            item = item,
            start_item = start_item,
            item_build = item_build,
            skill_order = skills,
            position = position,
            boots = boots,
        ).execute()

        logger.debug(f'****************{champion.name}\n{rune}\n{summ}\n{item}\n{start_item}\n{item_build}\n{skills}\n{boots}\n****************')

        logger.info(f'Champion: {champion}\tPosition: {position}\t{time.time() - start}')