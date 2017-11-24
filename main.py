from bottle import post, run, template, request, get
from blockchain import Blockchain

blockchain = Blockchain()


@get('/blocks')
def get_blocks():
    return template('<b>{{blocks}}</b>', blocks=blockchain.blocks)


@post('/mineBlock')
def mine_block():
    data = request.params.get('data')
    blockchain.add(data=data)
    return template('<b>add data:{{blocks}}</b>', blocks=blockchain.blocks[-1].data)


run(host='localhost', port=8000)
