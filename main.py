from bottle import post, run, template, request, get


@get('/hello')
def index():
    name = request.query.get('name')
    return template('<b>Hello {{name}}</b>', name=name)


@post('/hellopost')
def hello():
    name = request.forms.get('name')
    return template('<b>Hello {{name}}</b>', name=name)


run(host='localhost', port=8000)
