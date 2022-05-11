import sys

class FreshEnvironment:
    def __init__(self):
        self.old_modules = sys.modules

    def __enter__(self):
        sys.modules = {}
        return self

    def __exit__(self, *args):
        sys.modules = self.old_modules


class Tester:
    def __init__(self, test_cases)