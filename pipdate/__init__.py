"""Check for updates on PyPi.
"""

from .__about__ import __version__
from .main import check, get_pypi_version, needs_checking

__all__ = ["__version__", "needs_checking", "get_pypi_version", "check"]
