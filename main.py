import json
import argparse
import requests
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

    try:
        r = requests.get("http://" + url.hostname + ":" + str(url.port) + "/peers")
        if r.status_code == 200:
            p = Peer(url.hostname, url.port)
            peers.append(p)
            resp = {
                'type': QUERY_LATEST,
                'host': 'localhost:' + str(args.http_port)
            }
            p.send(data=resp)
    except ConnectionRefusedError:
        print("socket connection error")
    return


@get('/peers')
def get_peers():
    json_peers = json.dumps([str(p) for p in peers])
    return json_peers

@post('/websocket')
def websocket():
    print("websocket")
    data = json.load(request.body)
    message_handler(data)


def broadcast(resp):
    for p in peers:
        p.send(resp)


def start_httpserver():
    run(host='localhost', port=args.http_port)


def message_handler(message):
    if message["type"] == QUERY_LATEST:
        resp = {
            'type': RESPONSE_BLOCKCHAIN,
            'data': blockchain.blocks[-1].to_dict(),
        }
        #requests.post("http://"+message['host']+"/websocket", data=json.dumps(resp))
        requests.get("http://"+message['host']+"/peers")
    if message["type"] == QUERY_ALL:
        resp = {
            'type': RESPONSE_BLOCKCHAIN,
            'data': blockchain.blocks.to_dict(),
        }
        requests.post("http://"+message['host']+"/websocket", data=json.dumps(resp))
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
            resp = {
                'type': RESPONSE_BLOCKCHAIN,
                'data': [latest_block]
            }
            broadcast(resp)
        elif(len(received_blocks) == 1):
            resp = {
                'type': QUERY_ALL,
                'host': 'localhost:' + str(args.http_port)
            }
            broadcast(resp)
        else:
            blocks = [ Block.make_from_dict(b) for b in received_blocks]
            blockchain.replace(blocks)



start_httpserver()
