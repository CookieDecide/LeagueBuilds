import numpy, json, client
from models.statics_db import ITEMS

def info(champion, position):
    builds = client.get_builds(champion, position)

    runes = []
    summs = []
    stats = []
    items = []
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

    rune = sort_runes(runes)

    summ = sort_summs(summs)

    stat = sort_stats(stats)

    item = sort_items(items)

    return (rune|stat, summ, item)

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
    item, item_count = numpy.unique(items, return_counts=True)
    item_count_sort_ind = numpy.argsort(-item_count)
    sorted_items = []

    for i in item[item_count_sort_ind].tolist():
        element = ITEMS.get_or_none(ITEMS.id == i)
        if(element):
            if(element.into == '0' and '1001' not in element.from_ and 'Consumable' not in element.tags):
                sorted_items.append(i)

    return sorted_items