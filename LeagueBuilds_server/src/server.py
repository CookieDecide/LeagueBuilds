import socket
from models.dynamics_db import BUILDS
import json
import time
from threading import Thread

BUF_SIZE = 1024

def start_server():
    s = socket.socket()
    print("Socket successfully created")

    port = 12345

    s.bind(('', port))
    print("socket binded to %s" % (port))

    s.listen(5)
    print("socket is listening")

    while True:
        c = None

        try:
            c, addr = s.accept()

            client_thread = Thread(target=handle_client, args=(c,addr))
            client_thread.start()
        except:
            if c:
                c.close()
            break

def handle_client(c, addr):
    print('Got connection from', addr)
    msg = json.loads(c.recv(BUF_SIZE).decode())
    print(msg)

    if(msg[1]==''):
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
            BUILDS.championId == str(msg[0]),
            BUILDS.teamPosition != "",
            BUILDS.gameEndTimestamp >= time.time()*1000 - 1250000000,
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
            BUILDS.championId == str(msg[0]),
            BUILDS.teamPosition == msg[1],
            BUILDS.gameEndTimestamp >= time.time()*1000 - 1250000000,
        ).dicts()

    buffer = []
    for build in builds:
        buffer.append(build)

    msg = json.dumps(buffer).encode()
    c.send(msg)

    c.close()