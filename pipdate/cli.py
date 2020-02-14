import argparse
import sys

from .__about__ import __version__
from .update import update_all


def update(argv=None):
    parser = _get_parser()
    parser.parse_args(argv)
    update_all()


def _get_parser():
    parser = argparse.ArgumentParser(description=("Update all pip-installed packages."))

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"%(prog)s {__version__}, Python {sys.version}",
        help="display version information",
    )
    return parser
