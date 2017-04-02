# https://docs.python.org/3/distutils/setupscript.html
from setuptools import setup

name = 'slpyser'
description = 'Python 3 Library to parse SAPLink generated files, transforming it into objects.'
version = '0.0.1'
author = 'ThalesVB'
author_email = 'thalesvb@live.com'
url = 'http://www.github.com/thalesvb'
packages = [
    'slpyser',
    'slpyser.interface',
    'slpyser.model',
    'slpyser.model.abap_objects',
    'slpyser.model.saplink',
    'slpyser.xmlparser'
]


buildOptions = dict(
    build_base='./build/'
)

bdistOptions = dict(
    dist_dir='./bdist/'
)

sdistOptions = dict(
    dist_dir='./sdist/'
)

options = dict(
    build=buildOptions,
    bdist=bdistOptions,
    sdist=sdistOptions,
)

test_suite = 'tests'

setup(
    name=name,
    description=description,
    version=version,
    author=author,
    author_email=author_email,
    url=url,
    packages=packages,
    options=options,
    test_suite=test_suite,
)
