![PyPI - Status](https://img.shields.io/pypi/v/pytqshacl)

# Py(thon)T(op)Q(uadrant)SHA(pe)C(onstraint)L(anguage)

Python wrapper around [TopQuadrant's SHACL implementation](https://github.com/TopQuadrant/shacl) in Java.

## Why?

Motivation: This was developed as part of [BIM2RDF](https://github.com/PNNL/BIM2RDF)
where TopQuadrant was used to execute [SHACL](https://shacl-playground.zazuko.com/).
Python's [PySHACL](https://github.com/RDFLib/pySHACL) was too slow.
Nonetheless, it's useful to be able to integrate it with Python.


## Optional Features
can be installed as `pytqshacl[java,cli]`.
* Java: is installed on first use.
Note this changes your system. The installation location will be printed.
* CLI: will just wrap the topquadrant invocation with managed configuraion.

## Usage

Install [`pytqshacl`](https://pypi.org/project/pytqshacl/) with your Python package manager.
The features are optional `pytqshacl[cli,java]`.

### [CLI](./src/pytqshacl/cli.py)

Get help with `pytqshacl --help`.

Example usage:
```
pytqshacl\test on  master [!⇡] via  v3.11.9 
❯ pytqshacl validate -d data.ttl -s shapes.ttl -o None
ERRORS: process did not exit with 0

@prefix dash:    <http://datashapes.org/dash#> .     
@prefix graphql: <http://datashapes.org/graphql#> .  
@prefix owl:     <http://www.w3.org/2002/07/owl#> .  
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema:  <http://schema.org/> .
@prefix sh:      <http://www.w3.org/ns/shacl#> .     
@prefix swa:     <http://topbraid.org/swa#> .        
@prefix tosh:    <http://topbraid.org/tosh#> .       
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .

[ rdf:type     sh:ValidationReport ;
  sh:conforms  false ;
  sh:result    [ rdf:type                      sh:ValidationResult ;
                 sh:focusNode                  <https://example.com/John-Doe> ;
                 sh:resultMessage              "Property may only have 1 value, but found 2" ;
                 sh:resultPath                 schema:name ;
                 sh:resultSeverity             sh:Violation ;
                 sh:sourceConstraintComponent  sh:MaxCountConstraintComponent ;
                 sh:sourceShape                []    
               ]
] .
```

### [Lib](./src/pytqshacl/run.py)

Check the arguments from `validate` and `infer`
from the imports `from pytqshacl import validate, infer`.

### [Configuration](./src/pytqshacl/config.py)

The environment variable, `PYTQSHACL_PREFER_SYSJAVA`, can be set to 'false'
if the package is installed with the 'java' feature
to prefer finding a `java` executable in the system PATH environment variable.


## Dev Philosphy

This point of this code is just to provide access
to use TopQuadrant's SHACL from Python.
Therefore,

* No features: It should just wrap the TopQuadrant SHACL executable.
* No dependencies
