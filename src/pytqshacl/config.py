from os import environ as env
pts = 'pytqshacl'
envvar = f'{pts}_TQ_VER'
if envvar not in env:
    tqshacl_ver = '1.4.4'
else:
    tqshacl_ver = env[envvar]
assert(len(tqshacl_ver.split('.')) == 3)


envvar = f'{pts}_PREFER_SYSJAVA'
if envvar not in env:
    try:
        import jdk
        prefer_sysjava = False
    except ModuleNotFoundError: # did not want the option
        prefer_sysjava = True
else:
    _ = env[envvar].lower().strip()
    assert(_ in {'true', 'false'})
    if _ == 'true':     prefer_sysjava = True
    if _ == 'false':    prefer_sysjava = False


from types import SimpleNamespace as NS
config = NS(
    prefer_sysjava = prefer_sysjava,
    _tqshacl_ver = tqshacl_ver
)
__all__ = ['config']