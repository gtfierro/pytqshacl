from os import environ as env
envvar = 'PTS_TQ_VER'
if envvar not in env:
    tqshacl_ver = '1.4.2'
else:
    tqshacl_ver = env[envvar]
assert(len(tqshacl_ver.split('.')) == 3)
