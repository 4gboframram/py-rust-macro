# Getting Started
## Introduction
Many low-level languages have a concept of macros that allow users to not have to write the same code over and over again. 
In Python, however, there isn't such a feature.

Why would anyone want macros in Python? 
- Python is a very dynamic language and can be slow at times because of the overhead of calling the same function over and over
- You might want to add inline parsing of a language like `sql` to remove runtime overhead of parsing a literal
- Times you want to call a function before a script is run
- When you want to have access to an expression and its result at the same time in a safe way that doesn't have massive runtime overhead (eg. a testing library)

## Library Features

- A convenient way to provide import-time token generation and substitution through macros inspired by the `Rust` programming language
  
- An import hook that uses no external or platform-specific dependencies that can provide said functionality on any modern and compliant Python implementation running on any system.

- Tools for manipulating tokens and creating usable macros in a way that is more clear than the Python standard library
  
- A commandline utility that automatically runs the import hook

## Usage

With `Rust Macro`, it is easy to use macros from another module. Just put `# __use_macros__({modules})` on the first line of the file, where `modules` is a comma-separated list of string literals that contain the names of the modules you want to import from.

```{note}
The modules are imported in the exact same way as the standard Python import system except for a major difference; all macros are automatically brought into the module's macro namespace.
```

Macros can be then called within that same file with `{name}!({tokens})`.

Example:


```{code-block} default
---
lineno-start: 1
emphasize-lines: 1
caption: |
    (file hello.py)
---
# __use_macros__('rust_macro.builtins')

print(stringify!(Hello, World))
```

To run this file, there are 2 options. It can be run with `python3 -m rust_macro hello.py` or you can create another file to import the module from like so:


```
---
lineno-start: 1
caption: |
    (file hello.py)
---
from rust_macro import ExpandMacros

with ExpandMacros():
    import hello
```


Then you can simply run this main file by running `python3 main.py`

```{note}
The commandline utility approach sets the module's name to __main__ so that scripts can work properly. 
```

Both approaches are equally valid and usable, but the direct import approach is more embedable


Within the `ExpandMacros` context manager, all imported modules that have `# __use_macros__(args)` at the beginning of the file will have all macros expanded. This goes until all children modules' macros are expanded or until an exception is raised.

### Creating Your Own Macros
In a module that defines macros, a macro is nothing but a function that takes an `List[Token]` as a single parameter and either returns an `Iterable[Token]` or a `str`. .

When a `str` is returned, that string is then tokenized. **It is not converted into a string literal.**

To be able to export macros, define a variable named `__macros__` in the module's namespace that contains a mapping of names to a callable.

Example:
```
from rust_macro.util import Token
from typing import List

def macro(tokens: List[Token]) -> str:
    return "print('Hello, World!')"
    
__macros__ = {'macro': macro}
```

```{warning}
A macro call is not allowed to expand to another macro call
```

This file can then be used in an `# __use_macros__` statement and gives access to a macro named `macro`
