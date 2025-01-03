__version__ = "105"
from .topquadrant import ver as tq_ver
topquadrant_version = tq_ver
from .topquadrant.install import Java, Shacl
Java()
Shacl()
from .run import validate, infer
