from matplotlib.font_manager import json_load
import numpy, json, client, ast, datetime
from models.statics_db import ITEMS

valid_items = []
valid_start_items = []

def info(champion, position):
    builds = client.get_builds(champion, position)

    items_all = ITEMS.select()
    global valid_items
    global valid_start_items
    for item in items_all:
        if('Trinket' not in item.tags):
            valid_start_items.append(int(item.id))
            if(item.into == '0' and '1001' not in item.from_ and 'Consumable' not in item.tags):
                valid_items.append(int(item.id))

    runes = []
    summs = []
    stats = []
    items = []
    start_items = []
    items_build = []
    skills = []
    
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

        items.append(build['item0'])
        items.append(build['item1'])
        items.append(build['item2'])
        items.append(build['item3'])
        items.append(build['item4'])
        items.append(build['item5'])

        start_item_list = []
        for item in ast.literal_eval(build['start_items']):
            if(item['itemId'] in valid_start_items):
                start_item_list.append(item['itemId'])
        if(start_item_list):
            start_items.append(json.dumps(start_item_list))

        items_build_list = []
        for item in ast.literal_eval(build['items']):
            if(item['itemId'] in valid_items):
                items_build_list.append(item['itemId'])
        if(items_build_list and len(items_build_list)>2):
            items_build.append(json.dumps(items_build_list[0:3]))

        skills_list = []
        for skill in ast.literal_eval(build['skills']):
            skills_list.append(skill['skillSlot'])
        if(skills_list and len(skills_list)>3):
            skills.append(json.dumps(skills_list[0:4]))

    rune = sort_runes(runes)

    summ = sort_summs(summs)

    stat = sort_stats(stats)

    item = sort_items(items)

    start_item = sort_start_items(start_items)

    item_build = sort_items_build(items_build)

    skill_order = sort_skills(skills)

    return (rune|stat, summ, item, start_item, item_build, skill_order)

def sort_runes(runes):
    rune, rune_count = numpy.unique(runes, return_counts=True)

    return json.loads(rune[rune_count.tolist().index(max(rune_count))])

def sort_summs(summs):
    summ, summ_count = numpy.unique(summs, return_counts=True)
    summ_count_sort_ind = numpy.argsort(-summ_count)

    return summ[summ_count_sort_ind][0:2]

def sort_stats(stats):
    stat, stat_count = numpy.unique(stats, return_counts=True)

    return json.loads(stat[stat_count.tolist().index(max(stat_count))])

def sort_items(items):
    global valid_items
    item, item_count = numpy.unique(items, return_counts=True)
    item_count_sort_ind = numpy.argsort(-item_count)
    sorted_items = []

    for i in item[item_count_sort_ind].tolist():
        if(int(i) in valid_items):
            sorted_items.append(int(i))

    return sorted_items

def sort_start_items(start_items):
    start_item, start_item_count = numpy.unique(start_items, return_counts=True)
    start_item_count_sort_ind = numpy.argsort(-start_item_count)

    if (len(start_item[start_item_count_sort_ind])<3):
        return [json.loads(start_item[start_item_count_sort_ind][0])]
    else:
        return [json.loads(start_item[start_item_count_sort_ind][0]), json.loads(start_item[start_item_count_sort_ind][1]), json.loads(start_item[start_item_count_sort_ind][2])]

def sort_items_build(items_build):
    item_build, item_build_count = numpy.unique(items_build, return_counts=True)
    item_build_count_sort_ind = numpy.argsort(-item_build_count)

    if (len(item_build[item_build_count_sort_ind])<3):
        return [json.loads(item_build[item_build_count_sort_ind][0])]
    else:
        return [json.loads(item_build[item_build_count_sort_ind][0]), json.loads(item_build[item_build_count_sort_ind][1]), json.loads(item_build[item_build_count_sort_ind][2])]

def sort_skills(skills):
    skill, skill_count = numpy.unique(skills, return_counts=True)
    skill_count_sort_ind = numpy.argsort(-skill_count)

    return json.loads(skill[skill_count_sort_ind][0])