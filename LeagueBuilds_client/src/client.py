import requests
import datetime
import config
import json, ast

def get_build(champion, position, summoner):
    start = datetime.datetime.now()
              
    api_url = "http://" + config.server_ip + ":12345/builds/" + str(champion)
    if(position != ""):
        api_url += "/" +  str(position).lower()

    print(api_url)

    response = requests.get(api_url, headers={"Summoner":summoner}).json()

    print(response)

    print(datetime.datetime.now() - start)

    return response['championId'], ast.literal_eval(response['runes']), json.loads(response['summ']), json.loads(response['item']), json.loads(response['start_item']), json.loads(response['item_build']), json.loads(response['skill_order']), response['position'], response['champion'], json.loads(response['boots'])

def get_version():
    api_url = "http://" + config.server_ip + ":12345/version"

    print(api_url)

    response = requests.get(api_url).json()

    return response