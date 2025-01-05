# CLI

Run `pytqshacl  validate data.ttl --shapes shapes.ttl --out None`.
It should print:
```
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

# pytest

Just run `python test.py` in the [test dir](.).