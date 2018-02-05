import hashlib
import datetime
import json


class Blockchain():

    def __init__(self, blocks=None):
        # ジェネシスブロックを追加
        if blocks:
            self.blocks = blocks
            self.latest_index = len(blocks) - 1
        else:
            self.blocks = []
            self.latest_index = -1
            self.add(self.get_genesis_block())

    def __len__(self):
        return len(self.blocks)

    def get_latest_block(self):
        return self.blocks[-1]

    def add(self, block=None, data=None):

        # blockとdataの両方が指定されていない場合
        if not (block or data):
            return

        # dataが指定されている場合
        if not block:
            index = self.latest_index + 1
            previous_hash = self.blocks[-1].hash
            timestamp = int(datetime.datetime.timestamp(datetime.datetime.now()))
            hash = Block.calc_hash_from_args(index, previous_hash, timestamp, data)
            block = Block(index, previous_hash, timestamp, data, hash)

        # blockが有効ならばblocksに追加
        if len(self) == 0 or block.is_valid(self.blocks[-1]):
            self.blocks.append(block)
            self.latest_index += 1
        return

    def get_genesis_block(self):
        return Block(
            0,
            "0",
            1465154705,
            "my genesis block!!",
            "816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7"
        )

    def is_valid(self):
        if str(self.blocks[0]) != str(self.get_genesis_block()):
            return False
        for bl in self.blocks:
            if bl.index != 0 and not bl.is_valid(self.blocks[bl.index-1]):
                return False
        return True

    def replace(self, blocks):
        blockchain = Blockchain(blocks=blocks)
        if blockchain.is_valid() and len(blockchain) > len(self):
            self.blocks = blockchain.blocks
            self.latest_index = blockchain.blocks[-1].index

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return [b.to_dict() for b in self.blocks]


class Block():

    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def __repr__(self):
        return str(self.index) + self.previous_hash + str(self.timestamp) + self.data+self.hash

    def is_valid(self, pre_block):
        if pre_block.index + 1 != self.index:
            print("index")
            return False
        if pre_block.hash != self.previous_hash:
            print("previous_hash")
            return False
        if self.calc_hash() != self.hash:
            print("calc_hash")
            return False
        return True

    def calc_hash(self):
        return hashlib.sha256(
            (
                str(self.index) + self.previous_hash + str(self.timestamp) + str(self.data)
            ).encode('utf-8')
        ).hexdigest()

    def to_dict(self):
        return ({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": str(self.timestamp),
            "data": str(self.data),
            "hash": self.hash
        })

    @classmethod
    def make_from_dict(cls, dic):
        return cls(
            dic["index"],
            dic["previous_hash"],
            dic["timestamp"],
            dic["data"],
            dic["hash"]
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def calc_hash_from_args(cls, index, previous_hash, timestamp, data):
        return hashlib.sha256(
            (
                str(index) + previous_hash + str(timestamp) + str(data)
            ).encode('utf-8')
        ).hexdigest()
