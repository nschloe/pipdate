# -*- coding: utf-8 -*-
#
from setuptools import setup
import os
import codecs

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, 'pipdated', '__about__.py')) as f:
    exec(f.read(), about)


def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
            ).read()
    except Exception:
        content = ''
    return content


setup(
    name='pipdated',
    version=about['__version__'],
    packages=['pipdated'],
    url='https://github.com/nschloe/pipdated',
    download_url='https://pypi.python.org/pypi/pipdated',
    author=about['__author__'],
    author_email=about['__email__'],
    install_requires=[
        'appdirs',
        'requests'
        ],
    description='check for updates on PyPi',
    long_description=read('README.rst'),
    license=about['__license__'],
    classifiers=[
        about['__status__'],
        about['__license__'],
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Version Control',
        'Topic :: System :: Software Distribution',
        ],
    scripts=[
        'tools/pipdate',
        'tools/pipdate3'
        ]
    )
