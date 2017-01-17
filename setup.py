# -*- coding: utf-8 -*-
#
from distutils.core import setup
import os
import codecs

from pypi_version_checker import __version__, __license__, __author__, __email__


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
    name='pypi_version_checker',
    version=__version__,
    packages=['pypi_version_checker'],
    url='https://github.com/nschloe/pypi_version_checker',
    download_url='https://pypi.python.org/pypi/pypi_version_checker',
    author=__author__,
    author_email=__email__,
    requires=['requests'],
    description='check for updates on PyPi',
    long_description=read('README.rst'),
    license=__license__,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Version Control',
        'Topic :: System :: Software Distribution',
        ]
    )
