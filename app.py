import json

f = open('keys.json')
keys = json.load(f)
f.close()

def is_auth_succeed(env):
    #if env['REQUEST_METHOD'] != 'POST': return False
    #data = json.loads(env['wsgi.input'].read())
    for key in keys:
        if ('HTTP_COOKIE' in env
            and f'key={key}' in str(env['HTTP_COOKIE'])): return True
        elif ('QUERY_STRING' in env
            and f'key={key}' == str(env['QUERY_STRING'])): return True
    return False

def application(env, start_response):
    print(env)
    if not is_auth_succeed(env):
        start_response('401 OK', [('Content-Type', 'text/html')])
        return []

    start_response('200 OK', [('Content-Type','application/json')])

    if env['RAW_URI'].startswith('/api/state'):
        return get_state()
    if env['RAW_URI'].startswith('/api/remote'):
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
