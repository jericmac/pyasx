

import setuptools
import pypandoc


setuptools.setup(
    name='pyasx',
    version='1.0.0',
    description='Python library to pull data from ASX.com.au',
    long_description=pypandoc.convert('README.md', 'rst'),
    long_description_content_type='text/markdown',
    url='http://github.com/zacscott/pyasx',
    author='Zac Scott',
    author_email='zac@zacscott.net',
    license='MIT',
    packages=setuptools.find_packages(
        exclude=['tests',]
    ),
    python_requires='>=2.6',
    install_requires=[
        'requests',
        'pyyaml'
    ]
)
