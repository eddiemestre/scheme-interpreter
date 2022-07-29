# Python Scheme Interpreter

A scheme interpreter written in python. A lexical analyser (the core of which is scheme_tokens.py) paritions input strings into tokens while a syntactic analyzer (the core of which is scheme_reader.py) constructs an expression tree from the sequence of tokens. 

The Syntactical analyzer is tree-recursive and breaks down sequences of tokens into their subexpressions until meaning is reached. 

The interpreter can handle special forms and user-defined functions in addition to primitive data types and procedures. It also has a sense of local vs global scope and keeps track of these environment variables via dicts. 

Part of the Composing Programs curriculum at the University of California Berkeley. 