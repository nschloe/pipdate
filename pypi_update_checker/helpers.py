# -*- coding: utf-8 -*-
#
from distutils.version import LooseVersion
import requests
from sys import platform


class _bash_color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def check(name, installed_version, semantic_versioning=True):
    r = requests.get('https://pypi.python.org/pypi/%s/json' % name)
    if r.ok:
        data = r.json()
        upstream_version = data['info']['version']
        iv = LooseVersion(installed_version)
        uv = LooseVersion(upstream_version)
        if iv < uv:
            print(
                '>\n> Upgrade to   ' +
                _bash_color.GREEN +
                '%s %s' % (name, upstream_version) +
                _bash_color.END +
                '    available! (installed: %s)\n>' % installed_version
                )
            if semantic_versioning:
                # Check if the leftmost nonzero version number changed. If yes,
                # this means an API change according to Semantic Versioning.
                leftmost_changed = False
                for k in range(min(len(iv.version), len(uv.version))):
                    if iv.version[k] < uv.version[k]:
                        leftmost_changed = True
                        break
                if leftmost_changed:
                    print(
                       ('> %s\'s API changes in this upgrade. '
                        'Changes to your code may be necessary.\n>'
                        ) % name
                       )
            if platform == 'linux' or platform == 'linux2':
                print((
                    '> To upgrade %s with pip, type\n>\n'
                    '>    pip install -U %s\n>\n'
                    '> To upgrade all pip-installed packages, type\n>\n'
                    '>    pip freeze --local | grep -v \'^\-e\' | '
                    'cut -d = -f 1 | xargs -n1 pip install -U\n>'
                    ) % (name, name))
    return
