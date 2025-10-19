from pathlib import Path
def printerrs(s):
    if (s.returncode != 0):
        print('ERRORS: process did not exit with 0')
        print(s.stderr)
    return s.stdout

def _normalize_tool_args(tool_args):
    if tool_args is None:
        return None
    if isinstance(tool_args, (str, Path)):
        return (str(tool_args),)
    try:
        return tuple(str(a) for a in tool_args)
    except TypeError:
        return (str(tool_args),)

def common(  cmd,
        data,
        shapes,
        out,
        tool_args=None):
    data = Path(data)
    if shapes is not None: shapes = Path(shapes).as_posix()
    data = (data.as_posix())
    tool_args = _normalize_tool_args(tool_args)
    assert(cmd in {'infer', 'validate'})
    if cmd == 'infer': from     .run import infer       as f
    if cmd == 'validate': from  .run import validate    as f
    _ = f(data, shapes=shapes, tool_args=tool_args)
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
        out:Path | None =defaults.out,
        tool_args=None):
    return common('infer', data, shapes, out, tool_args=tool_args)
def validate(
        data: Path      =defaults.data,
        shapes:Path     =defaults.shapes,
        out:Path | None =defaults.out,
        tool_args=None):
    return common('validate', data, shapes, out, tool_args=tool_args)


from .run import cmd
try:
    from fire import Fire
except ModuleNotFoundError:
    raise ModuleNotFoundError("can't run cli. did you intend to install the feature pytqshacl[cli]?")
Fire({f.__name__:f for f in {cmd, validate, infer}})
exit(0)
