from rust_macro import ExpandMacros
import traceback


with ExpandMacros():

    try:
        open("main.py").read()

    except Exception as e:
        print(traceback.format_exc())
