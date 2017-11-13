import hashlib

class BlockChain():

	def __init__(self):
		self.blocks = []
		self.latest_index=-1
		#ジェネシスブロックを追加
		self.add(self.get_genesis_block())
		
	def add(self,block):
		# blockが有効ならばblocksに追加
		if len(self.blocks)==0 or block.is_valid(self.blocks[-1]):
			self.blocks.append(block)
			self.latest_index+=1
	def get_genesis_block(self):
		return Block	(0, 
				"0",
				 1465154705,
				 "my genesis block!!",
				 "816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7"
				)

class Block():
	
	def __init__(self,index,previous_hash,timestamp,data,hash):
		self.index=index
		self.previous_hash=previous_hash
		self.timestamp=timestamp
		self.data=data
		self.hash=hash
	def is_valid(self,pre_block):
		if pre_block.index+1 != self.index:
			return False
		if pre_block.hash != self.previous.hash:
			return False
		if self.calc_hash()!=self.hash:
			return False
		return True
		
	def calc_hash(self):
		return hashlib.sha256((str(self.index)+self.previous_hash+str(self.timestamp)+str(self.data)).encode('utf-8')).hexdigest()
