import socket
from models.builds_db import FINALBUILDS
from models.statics_db import CHAMPIONS
import json
from threading import Thread

BUF_SIZE = 1024

def start_server():
    s = socket.socket()
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    print("Socket successfully created")

    port = 12345

    s.bind(('192.168.178.89', port))
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

    if(msg[1]!=''):
        build = FINALBUILDS.get_or_none(
            FINALBUILDS.championId == str(msg[0]),
            FINALBUILDS.position != str(msg[1]).upper()
        )
        if(not build):
            build = FINALBUILDS.get_or_none(
                FINALBUILDS.championId == str(msg[0]),
                FINALBUILDS.position != ""
            )
    else:
        build = FINALBUILDS.get_or_none(
            FINALBUILDS.championId == str(msg[0]),
            FINALBUILDS.position != ""
        )

    buffer = {}
    buffer["championId"] =  build.championId
    buffer["runes"] =  build.runes
    buffer["summ"] =  build.summ
    buffer["item"] =  build.item
    buffer["start_item"] =  build.start_item
    buffer["item_build"] =  build.item_build
    buffer["skill_order"] =  build.skill_order
    buffer["position"] =  build.position
    buffer["champion"] =  CHAMPIONS.get(CHAMPIONS.key == build.championId).champion

    msg = json.dumps(buffer).encode()
    c.send(msg)

    c.close()
