from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence


def printerrs(proc):
    if proc.returncode != 0:
        print('ERRORS: process did not exit with 0')
        print(proc.stderr)
    return proc.stdout


def _normalize_tool_args(tool_args):
    if not tool_args:
        return None
    return tuple(str(arg) for arg in tool_args)


def common(cmd, data, shapes, out, tool_args:Sequence[str]|None=None):
    data = Path(data)
    if shapes is not None:
        shapes = Path(shapes).as_posix()
    data = data.as_posix()
    tool_args = _normalize_tool_args(tool_args)
    assert cmd in {'infer', 'validate'}
    if cmd == 'infer':
        from .run import infer as runner
    else:
        from .run import validate as runner
    proc = runner(data, shapes=shapes, tool_args=tool_args)
    stdout = printerrs(proc)
    if out is not None:
        Path(out).write_text(stdout)
        return out
    return stdout


class defaults:
    data = Path('data.ttl')
    shapes = Path('shapes.ttl')
    # better than None bc stdout could be mixed with errors/warnings
    out = Path('out.ttl')


def infer(
        data: Path = defaults.data,
        shapes: Path = defaults.shapes,
        out: Path | None = defaults.out,
        tool_args: Sequence[str] | None = None):
    return common('infer', data, shapes, out, tool_args=tool_args)


def validate(
        data: Path = defaults.data,
        shapes: Path = defaults.shapes,
        out: Path | None = defaults.out,
        tool_args: Sequence[str] | None = None):
    return common('validate', data, shapes, out, tool_args=tool_args)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='pytqshacl')
    sub = parser.add_subparsers(dest='command', required=True)

    def add_common(name: str):
        sp = sub.add_parser(name)
        sp.add_argument('-d', '--data', default=defaults.data, type=Path,
                        help='Path to the data graph (default: data.ttl).')
        sp.add_argument('-s', '--shapes', default=defaults.shapes, type=Path,
                        help='Path to the shapes graph (default: shapes.ttl).')
        sp.add_argument('-o', '--out', default=str(defaults.out),
                        help='Write results to this path; use "None" for stdout.')
        return sp

    add_common('infer')
    add_common('validate')
    return parser


def _maybe_path(value: str | Path | None) -> Path | None:
    if value in {None, 'None', 'none'}:
        return None
    return Path(value)


def cli(argv: Sequence[str] | None = None):
    parser = _build_parser()
    args, extra = parser.parse_known_args(argv)

    data = args.data
    shapes = args.shapes
    out = _maybe_path(args.out)
    tool_args = tuple(extra)

    if args.command == 'infer':
        result = infer(data=data, shapes=shapes, out=out, tool_args=tool_args)
    else:
        result = validate(data=data, shapes=shapes, out=out, tool_args=tool_args)

    if isinstance(result, str):
        print(result)
    return result


def main():
    return cli()


if __name__ == '__main__':
    sys.exit(cli())
