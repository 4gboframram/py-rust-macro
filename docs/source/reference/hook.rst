rust_macro.hook
======================

.. module:: rust_macro.hook

.. class:: ExpandMacros()


    The main class that provides a context manager interface to the main import hook.

    .. method:: __enter__() -> rust_macro.ExpandMacros
    
       Enables macro expansion on import

      :returns: self

    .. method:: __exit__(exception_type, exception_value, exception_traceback, /) -> None

       Disables macro expansion on import


.. exception:: MacroFindError(msg: str)

    An Exception that is raised when a module does not define macros when another module expects it.

    

    
.. exception:: MacroNotFoundError(name: str)

    A subclass of ``NameError`` that is raised when a macro cannot be found in the current scope.



.. class:: MacroExpander(fullname: str, path: str)

    A subclass of ``importlib.abc.SourceLoader`` that is responsible for processing macros in modules and loading processed modules

    .. warning::

       Do not use this class unless you know exactly what you are doing. If you do use this class, then do not call any of its methods directly. **This class's interface may change at any time and without warning.** The only guarantee is the existence of the methods ``MacroExpander.get_data`` and ``MacroExpander.get_filename`` and the class being a subclass of ``importlib.abc.SourceLoader``. This class may also be deprecated in the future.
       
    .. attribute:: fullname
        :type: str
        :value: fullname

        The full name of the module that ``self`` is responsible for loading

    .. attribute:: path
       :type: str
       :value: path

        The path of the module that ``self`` is responsible for loading

    .. attribute:: macros
       :type: dict[str, Callable[[Iterable[Token]], Union[Iterable[Token], str]]]
       :value: {}

       The mapping of names to macros that ``self`` uses to expand macros


    .. method:: add_macros(fullname: str) -> None:

       Update ``self``'s macro mapping with the contents of the module ``{fullname}.__macros__``.

       :param str fullname: The full name of the module to import macros from
       :raises MacroFindError: if the module at ``fullname`` does not have a ``__macros__`` atribute
       :raises ModuleNotFoundError: when the module path doesn't exist
        

    .. method:: get_filename(fullname: str) -> str

        Gets the path of the file that ``self`` is responsible for loading.

        :returns: ``self.path``


    .. method:: expand_macros(self, tokens: MutableSequence[Token]) -> MutableSequence[Token]

       Expands all registered macros in the token list

        :raises MacroNotFoundError: when there is an attempt to expand a macro that isn't defined in the current scope


    .. method:: recursive_expand(self, code: MutableSequence[Token], *, depth_limit: int = 50) -> MutableSequence[Token]

        Recursively expands macros that are in the token list.

        :raises MacroNotFoundError: when there is an attempt to expand a macro that isn't defined in the current scope
        :raises MacroError: when the ``depth_limit`` is exceeded


    .. method:: get_data(filename: str) -> str

        Gets the source code for the final processed module.

        :param str filename: the file path that is opened




    
