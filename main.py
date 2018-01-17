import json
import socket
import argparse
from urllib.parse import urlparse
from multiprocessing import Process


from bottle import post, run, request, get

from blockchain import Blockchain, Block

from server import Peer

from const import RESPONSE_BLOCKCHAIN, QUERY_LATEST, QUERY_ALL

parser = argparse.ArgumentParser(description='Pychain is an implementation of NaiveChain in Python3')
parser.add_argument('--http-port',
                    action='store',
                    default=8000,
                    type=int,
                    help='http port(default:8000)')
parser.add_argument('--socket-port',
                    action='store',
                    default=5000,
                    type=int,
                    help='socket port(default:5000)')
args = parser.parse_args()

blockchain = Blockchain()

peers = []


@get('/blocks')
def get_blocks():
    json_blockchain = blockchain.to_json()
    print(blockchain.blocks)
    return json_blockchain


@post('/mineBlock')
def mine_block():
    dic = json.load(request.body)
    blockchain.add(data=dic["data"])
    resp = {
        "type": RESPONSE_BLOCKCHAIN,
        "data": [blockchain.blocks[-1].to_dict()]
    }
    broadcast(resp)
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
    run(host='localhost', port=args.http_port)


p = Process(target=start_httpserver)
p.start()


s = socket.socket()

port = args.socket_port
s.bind(('', port))


def message_handler(message):
    if message["type"] == QUERY_LATEST:
        pass
    if message["type"] == QUERY_ALL:
        pass
    if message["type"] == RESPONSE_BLOCKCHAIN:
        handle_blockchain_response(message)


def handle_blockchain_response(message):
    global blockchain
    received_blocks = sorted(message["data"], key=lambda k: k["index"])
    latest_block = received_blocks[-1]
    my_latest_block = blockchain.get_latest_block()
    if latest_block["index"] > my_latest_block.index:
        if(my_latest_block.hash == latest_block["previous_hash"]):
            block = Block.make_from_dict(latest_block)
            blockchain.add(block=block)
            print(blockchain.blocks)
            resp = {
                'type': RESPONSE_BLOCKCHAIN,
                'data': [latest_block]
            }
            broadcast(resp)


while True:
    print('listening')
    s.listen(5)
    c, addr = s.accept()
    print('receving')
    recv = json.loads(c.recv(4096))
    message_handler(recv)
    c.close()
s.close()
p.join()
