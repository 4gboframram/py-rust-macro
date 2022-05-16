try:
    import _bootlocale

    _bootlocale  # pyflakes

    # fix for
    # AttributeError: module '_bootlocale' has no attribute 'getpreferredencoding'
    # on pypy3.7 when calling open with the import hook active
except ImportError:
    pass


import sys
import importlib
from importlib.abc import SourceLoader
from importlib.machinery import SourceFileLoader
from importlib.machinery import FileFinder
import tokenize as _tokenize
import ast
from typing import MutableSequence

from .util import untokenize, MacroError, tokenize_string, Token


class MacroFindError(Exception):
    """
    An Exception that is raised when a module does not have macros when another module expected it
    """

    def __init__(self, msg: str):
        super().__init__(msg)


class MacroNotFoundError(NameError):
    """
    An Exception that is raised when a macro cannot be found in the current scope.
    """

    def __init__(self, name: str):
        super().__init__(f"Macro {name!r} is not defined in the current scope!")


class ExpandMacros:
    """
    A context manager that allows expanding macros when importing a module.
    """

    def __init__(self, extension=(".py",)):
        self._path_hook = FileFinder.path_hook((MacroExpander, extension))

    def __enter__(self):
        sys.path_hooks.insert(0, self._path_hook)
        # clear any loaders that might already be in use by the FileFinder
        sys.path_importer_cache.clear()
        importlib.invalidate_caches()

        return self

    def __exit__(self, *args):
        sys.path_hooks = [i for i in sys.path_hooks if i is not self._path_hook]


class MacroExpander(SourceLoader):
    """
    The class responsible for expanding macros contained in a module. This class should not be instantiated directly and should only be used through ExpandMacros.
    """

    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path
        self.macros = {}

    def add_macros(self, fullname: str):
        """
        Adds macros from a module into self.macros
        """
        module = importlib.import_module(fullname)

        try:
            macros = module.__macros__
            self.macros.update(macros)
        except AttributeError as e:
            raise MacroFindError(
                f"Module {fullname!r} does not define any macros! Make sure __macros__ is set to a mapping of names to callables."
            ) from e

    def get_filename(self, fullname):
        return self.path

    def expand_macros(self, tokens: MutableSequence[Token]) -> MutableSequence[Token]:
        """
        Expands the macros in a string based on self.macros
        """

        (*tokens,) = filter(lambda x: x.string, tokens)

        i = 0

        while i < len(tokens):
            if tokens[i].string == "!":
                name_start = i - 1
                while (
                    " " in tokens[name_start].string
                ):  # ignore potential whitespace error tokens
                    name_start -= 1

                name_tok = tokens[name_start]

                if name_tok.type == _tokenize.NAME:

                    if not name_tok.string in self.macros:
                        raise MacroNotFoundError(name_tok.string)

                    i += 1

                    # get the end of the macro call
                    paren_level = 0
                    first_arg = i + 1

                    while True:
                        token = tokens[i]
                        if token.string == ")":
                            paren_level -= 1

                        elif token.string == "(":
                            paren_level += 1

                        i += 1

                        if not paren_level:
                            break

                    macro = self.macros[name_tok.string]
                    # macro.__globals__.update(self.locals)

                    new_toks = macro(tokens[first_arg : i - 1])

                    if isinstance(new_toks, str):
                        new_toks = tokenize_string(new_toks)

                    tokens[name_start:i] = new_toks
                    i = first_arg

            i += 1
        return tokens

    def recursive_expand(
        self, code: MutableSequence[Token], *, depth_limit: int = 50
    ) -> MutableSequence[Token]:
        """
        Recursively expands macros
        """
        unexpanded = ""
        depth = 0
        while code != unexpanded:
            unexpanded = code
            code = self.expand_macros(code)

            depth += 1
            if depth > depth_limit:
                raise MacroError("Macro recursion depth exceeded the limit")

        return untokenize(code)

    def get_data(self, filename: str) -> str:
        """Creates source code for the module"""
        with open(filename) as f:
            data = f.read()

        if data.startswith("# __use_macros__"):
            to_run = data.splitlines()[0].strip("# __use_macros__")
            to_run = ast.literal_eval(to_run)

            if isinstance(to_run, str):
                to_run = (to_run,)

            for file in to_run:
                self.add_macros(file)

            tokens = tokenize_string(data)
            return self.recursive_expand(tokens)
        else:
            return SourceFileLoader.get_data(self.path, filename)


__all__ = ["MacroFindError", "MacroNotFoundError", "ExpandMacros", "MacroExpander"]
