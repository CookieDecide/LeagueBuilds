import socket
import json, datetime, ast

BUF_SIZE = 10000000

def get_build(champion, position):
    start = datetime.datetime.now()
    s = socket.socket()
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    port = 12345               

    s.connect(('localhost', port))

    msg = json.dumps([champion, position]).encode()

    s.send(msg)

    msg = b''
    while True :
        data = s.recv(BUF_SIZE)
        msg += data
        if not data:
            break

    data = json.loads(msg.decode())

    s.close()
    print(datetime.datetime.now() - start)

    return data['championId'], ast.literal_eval(data['runes']), json.loads(data['summ']), json.loads(data['item']), json.loads(data['start_item']), json.loads(data['item_build']), json.loads(data['skill_order']), data['position'], data['champion']
    