import json

from bottle import post, run, template, request, get

from blockchain import Blockchain

blockchain = Blockchain()


@get('/blocks')
def get_blocks():
    json_blockchain = blockchain.to_json()
    return template(json_blockchain)


@post('/mineBlock')
def mine_block():
    dic = json.load(request.body)
    blockchain.add(data=dic["data"])
    return


run(host='localhost', port=8000)
