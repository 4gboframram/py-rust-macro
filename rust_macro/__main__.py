from . import MacroExpander, ExpandMacros
import sys


usage = """
Usage: python3 -m rust_macro [file]
Runs a python file while expanding its macros.
"""

with ExpandMacros():
    if len(sys.argv) == 2:
        loader: MacroExpander = MacroExpander("__main__", sys.argv[1])
        loader.load_module(loader.fullname)
    else:
        print(usage, file=sys.stderr)
