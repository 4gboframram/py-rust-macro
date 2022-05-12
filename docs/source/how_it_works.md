# How it Works
```{warning}
This section contains advanced information about how the library works internally that the average user might not care about. If you don't care how the library worls, you can skip this section and read the API documentation.
```

## `ExpandMacros`- The Main Entry Point
`ExpandMacros` is a context manager that has a single purpose - add the `MacroExpander` class to `sys.path_hooks` to hook imports and remove `MacroExpander` from`sys.path_hooks` when the user doesn't want the hook anymore. `ExpandMacros` does not contain any logic for hooking imports; it is all handled by `MacroExpander`

## `MacroExpander` - The Import Hook Itself

```{warning}
It is not recommended to use this class directly unless you know exactly what you're doing. 
```

- `MacroExpander` is a subclass of `importlib.abc.SourceLoader`. `SourceLoader` provides sensible default methods to load data from source code, but the method `get_data(path)` from `imporlib.abc.ResourceLoader` is the most important.

- `self.get_data(path)` checks the file if the file contains `# __use_imports__` and imports all of the modules. Then, it gathers all of the macros that are defined in each module's `__macros__`. If a module doesn't have `__macros__`, an Exception is raised. Then it calls `self.expand_macros()` on the file's contents

 - `self.expand_macros(code: str)` expands all of the macros in the file based on the keys in `self.macros`, calling the macro that processes the tokens, replacing the entire macro invokation with the result. 

- And then some `importlib` magic then turns the code from `self.get_data()` into the final module 