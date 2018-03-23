

import setuptools


setuptools.setup(
    name='pyasx',
    version='0.0.1',
    description='Python interface to pull ASX data directly from asx.com.au',
    url='http://github.com/zacscott/pyasx',
    author='Zac Scott',
    author_email='zac@zacscott.net',
    license='MIT',
    packages=['pyasx'],
    install_requires=[
        'requests',
        'pyyaml',
    ],
    zip_safe=False
)
