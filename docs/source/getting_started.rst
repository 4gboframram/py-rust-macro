# Rust-Macro: Simple Rust-Like Macros for Python
## Introduction
Many low-level languages have a concept of macros that allow users to not have to write the same code over and over again. 
In Python, however, there isn't such a feature.

Why would anyone want macros in Python? 
- Python is a very dynamic language and can be slow at times because of the overhead of calling the same function over and over
- You might want to add inline parsing of a language like `sql` to remove runtime overhead of parsing a literal
- Other times you want to call a function before the script is run


## Usage

Macros can be called with `{name}!({tokens})`.

To allow expanding macros, a `# __use_macros__(module_names)` must be placed at the start of the file. `module_names` contains the list of modules that contain macros that the module will use. The modules are found the same way as Python's import system


Example:

(hello.py)
```py
# __use_macros__('rust_macro.builtins')

print(stringify!(Hello, World))
```

To run this file, you have 2 options. You can run this file with `python3 -m rust_macro hello.py` or you can do the following:

(main.py)
```py
from rust_macro import ExpandMacros

with ExpandMacros():
    import hello
```
Then you can simply run `python main.py`

Within the `ExpandMacros` context manager, all imports that have `# __use_macros__(args)` at the beginning of the file will have all macros recursively expanded.

### Defining Custom Macros
In a file that defines macros, a macro is nothing but a function that takes an `List[Token]` and either returns an `Iterable[Token]` or a `str`. 
When a `str` is returned, that string is then tokenized.

To be able to export macros, define a variable named `__macros__` in the module that contains a mapping of names to a callable.

Example:
```py
from rust_macro.util import Token
from typing import List

def macro(tokens: List[Token]) -> str:
    return "print('Hello, World!')"
    
__macros__ = {'macro': macro}
```

This file can then be used in an `# __use_macros__` statement and gives access to a macro named `macro`


### Known Limitations
- Macros are not expanded recursively. A macro that expands into a macro call is not permitted.

