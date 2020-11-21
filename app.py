import json

f = open('passwd.txt')
passwd = f.read().strip()
f.close()

def is_auth_succeed(env):
    #if env['REQUEST_METHOD'] != 'POST': return False
    #data = json.loads(env['wsgi.input'].read())
    if ('HTTP_COOKIE' in env
        and str(env['HTTP_COOKIE']) == f'key={passwd}'): return True
    return False

def application(env, start_response):
    print(env)
    if not is_auth_succeed(env):
        start_response('401 OK', [('Content-Type', 'text/html')])
        return []

    start_response('200 OK', [('Content-Type','application/json')])

    if env['RAW_URI'] == '/api/state':
        return get_state()
    if env['RAW_URI'] == '/api/remote':
        return get_remote()

    return [b'']

def get_state():
    f = open('state.json', 'rb')
    state = f.read()
    return [state]

def get_remote():
    f = open('remote.json', 'rb')
    data = f.read()
    return [data]
