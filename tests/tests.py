import unittest
from types import ModuleType
import sys
import copy
import importlib
from pathlib import Path

from rust_macro import hook
from rust_macro import util


def module_from_code(name: str, code: str) -> ModuleType:
    module = ModuleType(name)
    exec(code, module.__dict__)
    return module


class CleanTest(unittest.TestCase):
    def setUp(self):
        self.old_modules = copy.copy(sys.modules)
        self.old_path_hooks = copy.copy(sys.path_hooks)

    def tearDown(self):
        del sys.modules
        del sys.path_hooks
        sys.modules = self.old_modules
        sys.path_hooks = self.old_path_hooks


class TestExpandMacro(CleanTest):
    def setUp(self):
        super().setUp()
        self.expander = hook.ExpandMacros()

    def test_setup_and_cleanup(self):
        with self.expander as e:
            self.assertIn(e._path_hook, sys.path_hooks, "failed to add the path hook")
            import dummy

        self.assertNotIn(
            self.expander._path_hook, sys.path_hooks, "cleaning up path hook failed"
        )

        self.assertIn("dummy", sys.modules, "failed to import dummy module")


class TestMacroExpander(CleanTest):
    def setUp(self):
        super().setUp()
        self.expander = hook.ExpandMacros()

    def test_add_macros(self):

        loader = hook.MacroExpander("", "")

        loader.add_macros("test_import.test_add_macros")
        with self.expander:
            import test_import.test_add_macros as m

            self.assertEqual(
                loader.macros,
                {"a_macro": m.this_is_a_macro},
                "macros were not added correctly",
            )

        loader.add_macros("test_import.test_add_macros2")

        with self.expander:
            import test_import.test_add_macros2 as mm

            self.assertEqual(
                loader.macros,
                {"a_macro": m.this_is_a_macro, "m": mm.this_is_a_macro},
                "macros were not added correctly",
            )

    def test_basic_expand_macros(self):
        loader = hook.MacroExpander("", "")

        loader.add_macros("rust_macro.builtins")

        inp = """
stringify!(Hello World)
print(stringify!(Hello World))       
        """
        data = [
            i.string
            for i in loader.expand_macros(util.tokenize_string(inp))
            if i.string
        ]

        s = """
'Hello World'
print('Hello World')
        """
        expected = [i.string for i in util.tokenize_string(s) if i.string]

        self.assertEqual(data, expected, "macro expansion acts up")
