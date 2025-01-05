from pathlib import Path
def printerrs(s):
    if (s.returncode != 0):
        print('ERRORS: process did not exit with 0')
        print(s.stderr)
    return s.stdout

def common(  cmd,
        data,
        shapes,
        out):
    data = Path(data)
    if shapes is not None: shapes = Path(shapes).as_posix()
    data = (data.as_posix())
    assert(cmd in {'infer', 'validate'})
    if cmd == 'infer': from     .run import infer       as f
    if cmd == 'validate': from  .run import validate    as f
    _ = f(data, shapes=shapes)
    rc = _.returncode
    _ = printerrs(_)
    if out is not None:
        open(out, 'w').write(_)
        return out
    else:
        return _

class defaults:
    data =      Path('data.ttl')
    shapes =    Path('shapes.ttl')
    # better than None bc stdout could be mixed with errors/warnings
    out =       Path('out.ttl')
def infer(
        data: Path      =defaults.data,
        shapes:Path     =defaults.shapes,
        out:Path | None =defaults.out):#Path('inferred.ttl')):
    return common('infer', data, shapes, out)
def validate(
        data: Path      =defaults.data,
        shapes:Path     =defaults.shapes,
        out:Path | None =defaults.out):#Path('inferred.ttl')):
    return common('validate', data, shapes, out)


from .run import cmd
try:
    from fire import Fire
except ModuleNotFoundError:
    raise ModuleNotFoundError("can't run cli. did you intend to install the feature pytqshacl[cli]?")
Fire({f.__name__:f for f in {cmd, validate, infer}})
exit(0)
