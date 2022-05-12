rust_macro.util
===============


.. module:: rust_macro.util


.. class:: Token

    :canonical: tokenize.TokenInfo

    A class that represents a token from the lexer. Iterables that yield these are taken in and returned by macros. This class is the same as ``tokenize.TokenInfo`` in the standard library.

    .. attribute:: type

        :type: int

        The type of token. See the Python  `token module <https://docs.python.org/3/library/token.html>`_ for all of the different options.


    .. attribute:: string

        :type: str

        The text that the token contains

    .. attribute:: start

        :type: int

    .. attribute:: end

        :type: int

    .. attribute:: line

        :type: str

        The line the token is located in


    .. property:: exact_type

        :type: int

        The exact type of token. See the Python `token module <https://docs.python.org/3/library/token.html>`_ for all of the different options.


.. exception MacroError(msg: str)

    An exception to be raised when a macro is invoked. 


.. function:: splitargs(tokens: Iterable[Token], *, delimiter: str = ",") -> List[List[Token]]

    Splits a group of tokens into parts by a delimiter string

    Example::

        from rust_macro.util import tokenize_string, splitargs

        tokens = tokenize_string("'Hello, World', Hello There")
        
        args = splitargs(tokens, delimiter=',')
        
        assert len(args) == 2
        assert args[0][0].string == "'Hello, World'"
        assert [i.string for i in args[1]] == ['Hello', 'There']

        

.. function:: fix(text: str) -> str

    Fixes a some wonky text created by ``tokenize.untokenize`` 


.. function:: untokenize(tokens: Iterable[Token]) -> str

    Converts on interable of Tokens back into a string.


.. function:: tokenize_string(s: str) -> List[Token]:

    Converts a string into its tokens

    

More may come soon! 

    