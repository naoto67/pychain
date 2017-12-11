import json

from blockchain import Blockchain


blockchain = Blockchain()

peers = []


class HTTPServer():

    def __init__(self):
        return

    def mine_block(self, data):
        blockchain.add(data=data)

    def get_blockchain(self):
        return blockchain.blocks

    def get_peers(self):
        return peers

    def add_peer(self, ip, port):
        peers.append(Peer(ip, port))


class P2PServer():

    def __init__(self):
        return


class Peer():

    def __init__(self, ip, port, socket):
        self.ip = ip
        self.port = port
        self.socket = socket

    def __repr__(self):
        return self.ip + ":" + str(self.port)

    def to_dict(self):
        return {
            "ip": self.ip,
            "port": self.port
        }

    def send(self, data):
        self.socket.send(str.encode(json.dumps(data)))
