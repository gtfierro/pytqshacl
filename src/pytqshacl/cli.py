from pathlib import Path


def printerrs(s):
    if (s.returncode != 0):
        print('ERRORS: process did not exit with 0')
        print(s.stderr)
    return s.stdout


def _clean_tool_args(tool_args):
    extras = tuple(str(arg) for arg in tool_args if arg not in {None, ''})
    return extras if extras else None


def common(cmd,
        data,
        shapes,
        out,
        *tool_args):
    data = Path(data)
    if shapes is not None: shapes = Path(shapes).as_posix()
    data = (data.as_posix())
    extras = _clean_tool_args(tool_args)
    assert(cmd in {'infer', 'validate'})
    if cmd == 'infer': from     .run import infer       as f
    if cmd == 'validate': from  .run import validate    as f
    _ = f(data, shapes=shapes, tool_args=extras)
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
        *tool_args):
    return common('infer', data, shapes, out, *tool_args)
def validate(
        data: Path      =defaults.data,
        shapes:Path     =defaults.shapes,
        out:Path | None =defaults.out,
        *tool_args):
    return common('validate', data, shapes, out, *tool_args)


from .run import cmd
try:
    from fire import Fire
except ModuleNotFoundError:
    raise ModuleNotFoundError("can't run cli. did you intend to install the feature pytqshacl[cli]?")
Fire({f.__name__:f for f in {cmd, validate, infer}})
exit(0)
