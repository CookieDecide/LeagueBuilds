import requests
import datetime
import config
import json, ast


def get_build(champion, position, summoner):
    # Request the most popular builds for champion and position from the LeagueBuilds server
    start = datetime.datetime.now()

    api_url = "http://" + config.server_ip + ":12345/builds_v1/" + str(champion)
    if position != "":
        api_url += "/" + str(position).lower()

    print(api_url)

    response = requests.get(api_url, headers={"Summoner": summoner}).json()

    print(response)

    print(datetime.datetime.now() - start)

    return (
        response["championId"],
        ast.literal_eval(response["runes"]),
        json.loads(response["summ"]),
        json.loads(response["item"]),
        json.loads(response["start_item"]),
        json.loads(response["item_build"]),
        json.loads(response["skill_order"]),
        response["position"],
        response["champion"],
        json.loads(response["boots"]),
    )


def get_version():
    # Request the current App Version used by the LeagueBuilds server
    api_url = "http://" + config.server_ip + ":12345/version"

    print(api_url)

    response = requests.get(api_url).json()

    return response
