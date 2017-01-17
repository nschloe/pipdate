# -*- coding: utf-8 -*-
#
import configparser
from datetime import datetime
from distutils.version import LooseVersion
import os
import requests
from sys import platform
import tempfile


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


def _get_sbc(config_file):

    if not os.path.exists(config_file):
        # add default config
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'SecondsBetweenChecks': 24*60*60,
            }
        with open(config_file, 'w') as configfile:
            config.write(configfile)

    # read config
    config = configparser.ConfigParser()
    config.read(config_file)

    return int(config['DEFAULT']['SecondsBetweenChecks'])


def check(name, installed_version, semantic_versioning=True):
    homedir = os.path.expanduser('~')
    config_file = os.path.join(homedir, '.pypi_update_checker')
    seconds_between_checks = _get_sbc(config_file)

    if seconds_between_checks < 0:
        # never check
        return

    # get the last time we checked and compare with seconds_between_checks
    logfile = os.path.join(
        tempfile.gettempdir(),
        'pypi_update_checker_last_check_time'
        )
    if os.path.exists(logfile):
        with open(logfile, 'r') as f:
            last_checked = datetime.strptime(
                f.readline(),
                '%Y-%m-%d %H:%M:%S'
                )
        timedelta = datetime.now() - last_checked
        if timedelta.total_seconds() < seconds_between_checks:
            # don't check yet
            return

    try:
        _check(
            name,
            installed_version,
            config_file=config_file,
            semantic_versioning=semantic_versioning,
            )
        # write timestamp to logfile
        sttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(logfile, 'w') as f:
            f.write(sttime)
    except RuntimeError:
        pass

    return


def get_pypi_version(name):
    r = requests.get('https://pypi.python.org/pypi/%s/json' % name)
    if not r.ok:
        raise RuntimeError('Response code %s.' % r.status_code)
    data = r.json()
    return data['info']['version']


def _check(name, installed_version, config_file, semantic_versioning):
    upstream_version = get_pypi_version(name)
    iv = LooseVersion(installed_version)
    uv = LooseVersion(upstream_version)
    if iv < uv:
        _print_update_warning(
            name,
            uv,
            iv,
            config_file,
            semantic_versioning
            )
    return


def _change_in_leftmost_nonzero(a, b):
    leftmost_changed = False
    for k in range(min(len(a), len(b))):
        if a[k] == 0 and b[k] == 0:
            continue
        leftmost_changed = (a[k] != b[k])
        break
    return leftmost_changed


def _print_update_warning(
        name,
        uv,
        iv,
        config_file,
        semantic_versioning
        ):
    print(
        '>\n> Upgrade to   ' +
        _bash_color.GREEN +
        '%s %s' % (name, uv.vstring) +
        _bash_color.END +
        '    available! (installed: %s)\n>' % iv.vstring
        )
    # Check if the leftmost nonzero version number changed. If yes,
    # this means an API change according to Semantic Versioning.
    if semantic_versioning and \
            _change_in_leftmost_nonzero(iv.version, uv.version):
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

    print(
        '> To disable these checks, '
        'set SecondsBetweenChecks in %s to -1.\n>' % config_file
        )

    return
