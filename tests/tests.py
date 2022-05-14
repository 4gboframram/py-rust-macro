import unittest
from types import ModuleType
import sys
import copy
import importlib
from pathlib import Path


from rust_macro import hook

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
            import math
            self.assertEqual(math.gcd(3, 2), 1, "Something is horribly wrong with the math module!") 

        self.assertNotIn(self.expander._path_hook, sys.path_hooks, "cleanup failed")

        self.assertIn('math', sys.modules, "failed to import math module")


class TestMacroExpander(CleanTest):

    def setUp(self):
        super().setUp()
        self.expander = hook.ExpandMacros()

    
    def test_add_macros(self):
        
        loader = hook.MacroExpander('', '')

        loader.add_macros('test_import.test_add_macros')
        with self.expander:
            import test_import.test_add_macros as m
            self.assertIs(m.__macros__['a_macro'], loader.macros['a_macro'], 'macros were not added correctly')

            self.assertEqual(loader.macros, {'a_macro': m.this_is_a_macro}, 'macros were not added correctly')

            self.assert
            
            
        
        
    
            