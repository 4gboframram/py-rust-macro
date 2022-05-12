import io
from tokenize import untokenize as ut, generate_tokens, TokenInfo as Token
import itertools
from typing import List, Iterable


class MacroError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def splitargs(
    tokens: Iterable[Token], delimiter: str = ","
) -> List[List[Token]]:  # typehinting is a bit broken
    """
    Splits a token stream into its args, separated by a delimiter
    """
    return [
        list(y)
        for x, y in itertools.groupby(tokens, lambda z: z.string == delimiter)
        if not x
    ]


def fix(text: str) -> str:
    """
    Fixes a bit of wonky text created by tokenize.untokenize
    """

    step1 = text.replace(" ,", ", ")
    return step1.strip()


def untokenize(tokens: Iterable[Token]) -> str:
    """
    Converts a token list back into a string
    """
    return fix(ut((i.type, i.string) for i in tokens))


def tokenize_string(s: str) -> List[Token]:
    """
    Tokenize a string into tokens
    """
    f = io.StringIO(s)
    return list(generate_tokens(f.readline))
