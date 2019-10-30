import argparse
import sys

from .__about__ import __version__
from .update import update_all


def update(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)
    update_all(args.user)


def _get_parser():
    parser = argparse.ArgumentParser(description=("Update all pip-installed packages."))

    parser.add_argument(
        "--user",
        action="store_true",
        default=False,
        help="Update packages in the user's home folder",
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s {}, Python {}".format(__version__, sys.version),
        help="display version information",
    )
    return parser
