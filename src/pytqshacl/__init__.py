__version__ = "141"
from .topquadrant import ver as tq_ver
topquadrant_version = tq_ver
from .run import validate, infer


def cli(argv=None):
    from .cli import cli as _cli
    return _cli(argv)
