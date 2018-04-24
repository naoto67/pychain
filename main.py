import json
import argparse
from urllib.parse import urlparse
from websocket import create_connection


import tornado.ioloop
import tornado.web
import tornado.websocket


from blockchain import Blockchain, Block

from server import Peer

from const import RESPONSE_BLOCKCHAIN, QUERY_LATEST, QUERY_ALL

parser = argparse.ArgumentParser(
        description='Pychain is an implementation of NaiveChain in Python3')
parser.add_argument('--http-port',
                    action='store',
                    default=8000,
                    type=int,
                    help='http port(default:8000)')
args = parser.parse_args()

blockchain = Blockchain()

peers = []


class BlockHandler(tornado.web.RequestHandler):
    def post(self):
        dic = json.loads(self.request.body)
        blockchain.add(data=dic["data"])
        resp = {
            "type": RESPONSE_BLOCKCHAIN,
            "data": [blockchain.blocks[-1].to_dict()]
        }
        broadcast(resp)
        return


class Blocks(tornado.web.RequestHandler):
    def get(self):
        json_blockchain = blockchain.to_json()
        print(blockchain.blocks)
        self.write(json_blockchain)


class addPeerHandler(tornado.web.RequestHandler):
    def post(self):
        dic = json.loads(self.request.body)
        url = urlparse(dic["peer"])
        try:
            sock = create_connection("ws://" + url.hostname + ":" + str(url.port) + "/websocket")
            p = Peer(url.hostname, url.port, sock)
            peers.append(p)
            resp = {
                'type': QUERY_LATEST,
                'host': 'localhost:' + str(args.http_port)
            }
            print("connection is success")
            p.send(data=resp)
        except ConnectionRefusedError:
            print("socket connection error")
        return


class Peers(tornado.web.RequestHandler):
    def get(self):
        json_peers = json.dumps([str(p) for p in peers])
        self.write(json_peers)


class WebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print('open websocket connection')

    def on_message(self, message):
        message = json.loads(message)
        if message["type"] == QUERY_LATEST:
            resp = {
                'type': RESPONSE_BLOCKCHAIN,
                'data': [blockchain.blocks[-1].to_dict()]
            }
            sock = create_connection("ws://" + message["host"] + "/websocket")
            sock.send(json.dumps(resp).encode('utf-8'))

        if message["type"] == QUERY_ALL:
            resp = {
                'type': RESPONSE_BLOCKCHAIN,
                'data': [blockchain.blocks.to_dict()]
            }
            sock = create_connection("ws://" + message["host"] + "/websocket")
            sock.send(json.dumps(resp).encode('utf-8'))
        if message["type"] == RESPONSE_BLOCKCHAIN:
            handle_blockchain_response(message)

    def close(self):
        print("close websocket connection")


def broadcast(resp):
    for p in peers:
        p.send(resp)


def handle_blockchain_response(message):
    received_blocks = sorted(message["data"], key=lambda k: k["index"])
    latest_block = received_blocks[-1]
    print(type(latest_block))
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
            blocks = [Block.make_from_dict(b) for b in received_blocks]
            blockchain.replace(blocks)


application = tornado.web.Application([
    (r"/mineBlock", BlockHandler),
    (r"/blocks", Blocks),
    (r"/addPeer", addPeerHandler),
    (r"/peers", Peers),
    (r"/websocket", WebSocket),
])


if __name__ == "__main__":
    application.listen(args.http_port)
    tornado.ioloop.IOLoop.instance().start()
