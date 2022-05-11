from rust_macro.util import Token
from typing import List

def macro(tokens: List[Token]) -> str:
    return "print('Hello, World!')"
    
__macros__ = {'macro': macro}