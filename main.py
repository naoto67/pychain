import json
import socket
from urllib.parse import urlparse
from multiprocessing import Process


from bottle import post, run, request, get

from blockchain import Blockchain

from server import Peer

from const import RESPONSE_BLOCKCHAIN


blockchain = Blockchain()

peers = []


@get('/blocks')
def get_blocks():
    json_blockchain = blockchain.to_json()
    return json_blockchain


@post('/mineBlock')
def mine_block():
    dic = json.load(request.body)
    blockchain.add(data=dic["data"])
    resp = {
        "type": RESPONSE_BLOCKCHAIN,
        "data": blockchain.blocks[-1].to_dict()
    }
    broadcast(json.dumps(resp))
    return


@post('/addPeer')
def add_peer():
    dic = json.load(request.body)
    url = urlparse(dic["peer"])
    ws = socket.socket()
    try:
        ws.connect((url.hostname, url.port))
        peers.append(Peer(url.hostname, url.port, ws))
    except ConnectionRefusedError:
        print("socket connection error")
        ws.close()
    return


@get('/peers')
def get_peers():
    json_peers = json.dumps([str(p) for p in peers])
    return json_peers


def broadcast(resp):
    for p in peers:
        p.send(resp)


def start_httpserver():
    run(host='localhost', port=8000)


p = Process(target=start_httpserver)
p.start()


s = socket.socket()

port = 5000
s.bind(('', port))

while True:
    print('listening')
    s.listen(5)
    c, addr = s.accept()
    print('receving')
    print(c.recv(4096))
    c.close()
s.close()
p.join()
