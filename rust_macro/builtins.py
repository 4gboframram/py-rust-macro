import tokenize
from ast import literal_eval
from typing import Iterable, Union, NoReturn
from .util import untokenize, MacroError, Token
import sys
import platform


def stringify(tokens: Iterable[Token]) -> str:
    """
    Converts the tokens passed into a string literal
    """
    return repr(untokenize(tokens))


def include(tokens: Iterable[Token]) -> str:

    if len(tokens) != 1 and tokens[0].type != tokenize.STRING:
        raise MacroError("include!() expected a single string literal")
    path = literal_eval(tokens[0].string)
    with open(path) as f:
        code = f.read()
    return code


def include_str(tokens: Iterable[Token]) -> str:
    return repr(include(tokens))


def include_bytes(tokens: Iterable[Token]) -> str:
    if len(tokens) != 1 and tokens[0].type != tokenize.STRING:
        raise MacroError("include_bytes!() expected a single string literal")
    path = literal_eval(tokens[0].string)
    with open(path, "rb") as f:
        code = f.read()
    return repr(code)


def platform_mac(tokens: Iterable[Token]) -> Union[str, Iterable[Token]]:
    """
    If sys.platform starts with the specified string, return the code. Otherwise, deletes the code.

    Example:
        platform!("linux", print("linux"))
    """
    string = untokenize(tokens)
    parts = string.split(",")
    if len(parts) <= 1:
        raise MacroError(
            "platform!() expected a string literal and code separated by a comma"
        )

    platform_str = literal_eval(parts[0])

    if sys.platform.startswith(platform_str):
        return ",".join(parts[1:])

    return []


def python_impl(tokens: Iterable[Token]) -> Union[str, Iterable[Token]]:
    """
    If platform.python_implementation() matches specified string, return the code. Otherwise, deletes the code.

    Example:
        python_impl!("pypy", print("pypy"))
    """
    string = untokenize(tokens)
    parts = string.split(",")
    if len(parts) <= 1:
        raise MacroError(
            "python_impl!() expected a string literal and code separated by a comma"
        )

    impl_str = literal_eval(parts[0])

    if platform.python_implementation().lower() == impl_str:
        return ",".join(parts[1:])

    return []


def py_gte(tokens: Iterable[Token]) -> Union[str, Iterable[Token]]:
    """
    If sys.version_info >= the version specified (as a string literal) then return the code. Otherwise, deletes the code.

    Example:
        py_gte!("3.5", print("3.5"))
    """
    string = untokenize(tokens)

    parts = string.split(",")
    if len(parts) <= 1:
        raise MacroError(
            "py_gte!() expected a string literal and code separated by a comma"
        )

    version_string = literal_eval(parts[0])

    version_tuple = tuple(int(i) for i in version_string.split("."))

    if sys.version_info >= version_tuple:
        return ",".join(parts[1:])

    return []


def compile_error(tokens: Iterable[Token]) -> NoReturn:
    """
    raises a compile error upon expanding. probably not useful.
    """
    if len(tokens) != 1 and tokens[0].type != tokenize.STRING:
        raise MacroError("compile_error!() expected a single string literal")

    msg = literal_eval(tokens[0].string)
    raise MacroError(msg)


__macros__ = {
    "stringify": stringify,
    "include": include,
    "include_str": include_str,
    "include_bytes": include_bytes,
    "platform": platform_mac,
    "python_impl": python_impl,
    "py_gte": py_gte,
    "compile_error": compile_error,
}
