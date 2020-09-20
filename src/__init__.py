# https://stackoverflow.com/a/29714764
import os
import pkgutil

__path__ = [x[0] for x in os.walk(os.path.dirname(__file__))]


def load_tests(loader, suite, pattern):
    for imp, modname, _ in pkgutil.walk_packages(__path__):
        for test in loader.loadTestsFromModule(imp.find_module(modname).load_module(modname)):
            suite.addTests(test)
    return suite
