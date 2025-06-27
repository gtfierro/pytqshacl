from pathlib import Path
from typing import Literal

def env():
    from os import environ
    from .topquadrant.install import Shacl
    si = Shacl()
    return {**environ,
        'SHACL_HOME': str(si.home),
        'SHACL_CP': f"{si.lib}/*", # need a star for some reason
        'LOGGING': str(si.logging),
          }

NOTSET = object()
def tryenv(k):
    # ugly
    try:
        return env()[k]
    except KeyError:
        return NOTSET

def cmd(
        cmd:Literal['validate']|Literal['infer'],
        datafile: Path,
        shapesfile: Path=None,
        shacl_cp=tryenv('SHACL_CP'), jvm_args='', logging=tryenv('LOGGING'),
        ):
    """command passed to java to run topquadrant shacl."""
    assert(cmd in {'validate', 'infer'})
    if (shacl_cp == NOTSET) or (logging == NOTSET):
        raise EnvironmentError("shacl_cp or logging not set")
    
    logging = f"-Dlog4j.configurationFile={logging}" if logging else ''
    # class path
    # quote so no funny shell parsing happens (on linux)
    shacl_cp = f"-cp \"{shacl_cp}\"" 
    cmd = cmd[0].upper()+cmd[1:]
    from .topquadrant.install import Java
    java = Java.get()
    assert(java)
    cmd = f"{java} {jvm_args} {logging} {shacl_cp} org.topbraid.shacl.tools.{cmd}"
    _ = f"{cmd} -datafile {datafile} "
    if shapesfile:
        _ = _+f"-shapesfile {shapesfile}"
    return _

import logging
logger = logging.getLogger('topquadrant')
def check_proc_manually(cmd, proc):
    # further guard to fail
    # in case topquadrant does not exit with an error
    # that's why check is false below
    if any(w in proc.stderr.lower() for w in {'exception', 'error'}):
        from subprocess import CalledProcessError
        from sys import stderr
        print(proc.stderr, file=stderr)
        raise CalledProcessError(proc.returncode, cmd, stderr=proc.stderr)
    
    # filter out warnings to *hop* valid ttl of stdout
    _ = []
    for l in proc.stdout.split('\n'):
        ll:str = l.lower().strip()
        if      (('warn' and 'riot') in ll) \
            or  (' WARN ' in l) \
            or  ('org.apache.jena' in l)\
            or  ('org.topbraid.shacl' in l)\
            or  ('jdk.' in l)\
            or  ('java.' in l)\
            or  (l.startswith('at '))\
            or  (ll.startswith('caused by'))\
            or  (ll.startswith('...') and ll.endswith('more')):
            logger.warning(l)
        else:
            _.append(l)
    proc.stdout = MaybeInvalidTTL('\n'.join(_))
    return proc

class MaybeInvalidTTL(str): ...


def common(cmdnm, data, shapes):
    c = cmd(cmdnm, data, shapes)
    from subprocess import run
    _ = run(
            c, check=False, env=env(), shell=True,
            capture_output=True, text=True )
    _ = check_proc_manually(c, _)
    return _

def validate(data: Path, *, shapes:Path|None=None):
    _ = common('validate', data, shapes)
    return _
def infer(data: Path, *, shapes:Path|None=None):
    _ = common('infer', data, shapes)
    return _
