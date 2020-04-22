import argparse
import sys

from .__about__ import __version__
from .update import update_all


def update(argv=None):
    parser = argparse.ArgumentParser(description=("Update all pip-installed packages."))
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"pipdate {__version__}, Python {sys.version}",
        help="display version information",
    )
    parser.parse_args(argv)
    update_all()


if __name__ == "__main__":
    update(sys.argv[1:])
