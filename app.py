import json

f = open('passwd.txt')
passwd = f.read().strip()
f.close()

def is_auth_succeed(env):
    if env['REQUEST_METHOD'] != 'POST': return False
    data = json.loads(env['wsgi.input'].read())
    if 'passwd' in data and str(data['passwd']) == passwd: return True
    return False

def application(env, start_response):
    if not is_auth_succeed(env):
        start_response('401 OK', [('Content-Type', 'text/html')])
        return []

    start_response('200 OK', [('Content-Type','application/json')])
    f = open('state.json', 'rb')
    state = f.read()
    return [state]
