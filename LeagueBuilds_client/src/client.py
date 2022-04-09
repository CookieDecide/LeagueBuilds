import socket
import json, datetime

BUF_SIZE = 4096

def get_builds(champion, position):
    s = socket.socket()
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    port = 12345               

    s.connect(('decide.hopto.org', port))

    msg = json.dumps([champion, position]).encode()

    s.send(msg)

    msg = b''
    while True :
        data = s.recv(BUF_SIZE)
        msg += data
        if not data:
            break

    s.close
    return json.loads(msg.decode())
    