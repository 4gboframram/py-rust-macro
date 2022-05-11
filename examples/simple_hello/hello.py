# __use_macros__('rust_macro.builtins')

# you can run either main.py or
# python -m rust_macro hello.py

if __name__ == '__main__':
    print(stringify!(Hello, World))