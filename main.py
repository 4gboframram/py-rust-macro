from rust_macro.util import tokenize_string, splitargs

tokens = tokenize_string("'Hello, World', Hello There")

args = splitargs(tokens, delimiter=',')

assert len(args) == 2
assert args[0][0].string == "'Hello, World'"
assert [i.string for i in args[1]] == ['Hello', 'There']