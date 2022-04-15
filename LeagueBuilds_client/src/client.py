import socket
import json, datetime

BUF_SIZE = 10000000

def get_builds(champion, position):
    start = datetime.datetime.now()
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

    s.close()
    print(datetime.datetime.now() - start)
    return json.loads(msg.decode())
    
