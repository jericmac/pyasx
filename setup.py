

import setuptools

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = open("README.md").read()
    print("NOTE documentation not generated correctly, requires `pypandoc`")


setuptools.setup(
    name='pyasx',
    version='2.1.7',
    description='Python library to pull data from ASX.com.au',
    long_description=long_description,
    url='http://github.com/zacscott/pyasx',
    author='Zac Scott',
    author_email='zac@zacscott.net',
    license='MIT',
    packages=setuptools.find_packages(
        exclude=['tests',]
    ),
    package_data={'pyasx': ['*.yml']},
    python_requires='>=2.6',
    install_requires=[
        'requests',
        'pyyaml',
        'python-dateutil'
    ]
)
