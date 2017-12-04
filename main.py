import json
from urllib.parse import urlparse

from bottle import post, run, request, get

from blockchain import Blockchain

from server import Peer


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
    return


@post('/addPeer')
def add_peer():
    dic = json.load(request.body)
    url = urlparse(dic["peer"])
    peers.append(Peer(url.hostname, url.port))


@get('/peers')
def get_peers():
    json_peers = json.dumps([str(p) for p in peers])
    return json_peers


run(host='localhost', port=8000)
