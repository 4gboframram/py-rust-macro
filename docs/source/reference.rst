API Reference
=============

The API is currently made up of 3 modules:

    ``rust_macro.hook`` - The place where the magic happens

    ``rust_macro.util`` - Utilities for working with tokens and creating macros

    ``rust_macro.builtins`` - A bunch of useful default macros

    .. note:: 
        
        ``rust_macro`` exports all names from ``rust_macro.util`` and ``rust_macro.hook``


.. toctree::
   :maxdepth: 2
   :includehidden:

   reference/hook
   reference/util
   reference/builtin