from fire import Fire
from pathlib import Path
def printerrs(s):
    if (s.returncode != 0):
        print('ERRORS')
        print(s.stderr)
    return s.stdout

class defaults:
    data =      Path('data.ttl')
    shapes =    Path('shapes.ttl')
    # better than None bc stdout could be mixed with errors
    out =       Path('out.ttl')

def common(  cmd,
        data,
        shapes,
        out):
    data = Path(data)
    shapes = Path(shapes)
    data = (data.as_posix())
    shapes = (shapes.as_posix())
    assert(cmd in {'infer', 'validate'})
    if cmd == 'infer': from .run import infer as f
    if cmd == 'validate': from .run import infer as f
    _ = f(data, shapes)
    rc = _.returncode
    _ = printerrs(_)
    if out is not None:
        open(out, 'w').write(_)
        return out
    else:
        return _

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
Fire({f.__name__:f for f in {cmd, validate, infer}})
exit(0)
