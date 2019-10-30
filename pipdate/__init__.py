"""Check for updates on PyPi.
"""

from .__about__ import __author__, __copyright__, __email__, __license__, __version__
from .main import check, get_pypi_version, needs_checking

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
