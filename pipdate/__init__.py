# -*- coding: utf-8 -*-
#
"""Check for updates on PyPi.
"""

from .__about__ import __author__, __email__, __copyright__, __license__, __version__

from .main import needs_checking, get_pypi_version, check

__all__ = [
    "__author__",
    "__email__",
    "__copyright__",
    "__license__",
    "__version__",
    "needs_checking",
    "get_pypi_version",
    "check",
]
