from os import environ as env
envvar = 'PTS_TQ_VER'
if envvar not in env:
    tqshacl_ver = '1.4.2'
else:
    tqshacl_ver = env[envvar]
assert(len(tqshacl_ver.split('.')) == 3)


envvar = 'PTS_PREFER_SYSJAVA'
if envvar not in env:
    prefer_sysjava = True
else:
    _ = env[envvar].lower()
    assert(_ in {'true', 'false'})
    if _ == 'true':     prefer_sysjava = True
    if _ == 'false':    prefer_sysjava = False

