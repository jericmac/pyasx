#!/usr/bin/env python


import unittest
import pyasx.test.data.company
import pyasx.test.data.historical
import pyasx.test.data.share


test_modules = [
    pyasx.test.data.company,
    pyasx.test.data.historical,
    pyasx.test.data.share
]


# build the test suite automatically based on the configured test_modules above

loader = unittest.TestLoader()
suite  = unittest.TestSuite()

for test_module in test_modules:
    suite.addTests(loader.loadTestsFromModule(test_module))

# run the test suite
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
