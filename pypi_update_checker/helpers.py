# -*- coding: utf-8 -*-
#
from pypi_update_checker.meta import __name__ as name
from pypi_update_checker.meta import __author__ as author

import appdirs
import configparser
from datetime import datetime
from distutils.version import LooseVersion
import json
import os
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


_config_dir = appdirs.user_config_dir(name)
if not os.path.exists(_config_dir):
    os.makedirs(_config_dir)
_config_file = os.path.join(_config_dir, 'config.ini')

_log_dir = appdirs.user_log_dir(name, author)
if not os.path.exists(_log_dir):
    os.makedirs(_log_dir)
_log_file = os.path.join(_log_dir, 'times.log')


def _get_seconds_between_checks():
    if not os.path.exists(_config_file):
        # add default config
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'SecondsBetweenChecks': 24*60*60,
            }
        with open(_config_file, 'w') as handle:
            config.write(handle)

    # read config
    config = configparser.ConfigParser()
    config.read(_config_file)

    return int(config['DEFAULT']['SecondsBetweenChecks'])


def _get_last_check_time(name):
    if not os.path.exists(_log_file):
        return None
    with open(_log_file, 'r') as handle:
        d = json.load(handle)
        if name in d:
            last_checked = datetime.strptime(
                d[name],
                '%Y-%m-%d %H:%M:%S'
                )
        else:
            return None
    return last_checked


def _log_time(name, time):
    if os.path.exists(_log_file):
        with open(_log_file, 'r') as handle:
            d = json.load(handle)
    else:
        d = {}

    d[name] = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(_log_file, 'w') as handle:
        json.dump(d, handle)
    return


def needs_checking(name):
    seconds_between_checks = _get_seconds_between_checks()

    if seconds_between_checks < 0:
        return False

    # get the last time we checked and compare with seconds_between_checks
    last_checked = _get_last_check_time(name)
    if last_checked is not None and \
            (datetime.now() - last_checked).total_seconds() \
            < seconds_between_checks:
        return False

    return True


def get_pypi_version(name):
    r = requests.get('https://pypi.python.org/pypi/%s/json' % name)
    if not r.ok:
        raise RuntimeError('Response code %s.' % r.status_code)
    data = r.json()
    return data['info']['version']


def check_and_notify(name, installed_version, semantic_versioning=True):
    try:
        upstream_version = get_pypi_version(name)
    except RuntimeError:
        return

    iv = LooseVersion(installed_version)
    uv = LooseVersion(upstream_version)
    if iv < uv:
        _print_warning(name, iv, uv, semantic_versioning=semantic_versioning)
        _log_time(name, datetime.now())

    return


def _change_in_leftmost_nonzero(a, b):
    leftmost_changed = False
    for k in range(min(len(a), len(b))):
        if a[k] == 0 and b[k] == 0:
            continue
        leftmost_changed = (a[k] != b[k])
        break
    return leftmost_changed


def _print_warning(name, iv, uv, semantic_versioning):
    print(
        '>\n> Upgrade to   ' +
        _bash_color.GREEN +
        '%s %s' % (name, uv.vstring) +
        _bash_color.END +
        '    available! (installed: %s)\n>' % iv.vstring
        )
    # Check if the leftmost nonzero version number changed. If yes, this means
    # an API change according to Semantic Versioning.
    if semantic_versioning and \
            _change_in_leftmost_nonzero(iv.version, uv.version):
        print(
           ('> ' +
            _bash_color.YELLOW +
            '%s\'s API changes in this upgrade. '
            'Changes to your code may be necessary.\n' +
            _bash_color.END +
            '>'
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
        'set SecondsBetweenChecks in %s to -1.\n>' % _config_file
        )

    return
