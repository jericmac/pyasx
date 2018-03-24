

import setuptools


setuptools.setup(
    name='pyasx',
    version='1.0.0-pre',
    description='Python interface to pull ASX data directly from asx.com.au',
    url='http://github.com/zacscott/pyasx',
    author='Zac Scott',
    author_email='zac@zacscott.net',
    license='MIT',
    packages=['pyasx'],
    python_requires='>=2.6',
    install_requires=[
        'requests',
        'pyyaml'
    ],
    zip_safe=False
)
