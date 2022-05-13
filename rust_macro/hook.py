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

from .util import untokenize, tokenize_string


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

    def expand_macros(self, code: str) -> str:
        """
        Expands the macros in a string based on self.macros
        """
        tokens = tokenize_string(code)

        i = 0
        while i < len(tokens):
            if tokens[i].string == "!":
                name_start = i - 1
                previous_tok = tokens[name_start]

                if previous_tok.type == _tokenize.NAME:

                    if not previous_tok.string in self.macros:
                        raise MacroNotFoundError(previous_tok.string)

                    i += 1
                    level = 0
                    first_arg = i + 1
                    while True:

                        if tokens[i].string == ")":
                            level -= 1

                        elif tokens[i].string == "(":
                            level += 1
                        i += 1
                        if not level:
                            break

                    macro = self.macros[previous_tok.string]
                    # macro.__globals__.update(self.locals)

                    new_toks = macro(tokens[first_arg : i - 1])

                    if isinstance(new_toks, str):
                        new_toks = tokenize_string(new_toks)

                    tokens[name_start:i] = new_toks
                    i = first_arg

            i += 1
        return untokenize(tokens)

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

            return self.expand_macros(data)
        else:
            return SourceFileLoader.get_data(self.path, filename)
