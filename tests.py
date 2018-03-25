#!/usr/bin/env python


import unittest
import pyasx.tests.data.companies
import pyasx.tests.data.securities


test_modules = [
    pyasx.tests.data.companies,
    pyasx.tests.data.securities
]

# build the test suite automatically based on the configured test_modules above

loader = unittest.TestLoader()
suite  = unittest.TestSuite()

for test_module in test_modules:
    suite.addTests(loader.loadTestsFromModule(test_module))

# run the test suite
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
