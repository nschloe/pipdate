# -*- coding: utf-8 -*-
#
# pylint: disable=too-few-public-methods,no-name-in-module,import-error
from datetime import datetime
from distutils.version import LooseVersion
import json
import os
import sys

import appdirs

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


_config_dir = appdirs.user_config_dir('pipdate')
if not os.path.exists(_config_dir):
    os.makedirs(_config_dir)
_config_file = os.path.join(_config_dir, 'config.ini')

_log_dir = appdirs.user_log_dir('pipdate', u'Nico Schlömer')
if not os.path.exists(_log_dir):
    os.makedirs(_log_dir)
_log_file = os.path.join(_log_dir, 'times.log')


def _get_seconds_between_checks():
    if not os.path.exists(_config_file):
        # add default config
        parser = configparser.ConfigParser()
        parser.set('DEFAULT', 'SecondsBetweenChecks', str(24*60*60))
        with open(_config_file, 'w') as handle:
            parser.write(handle)

    # read config
    config = configparser.ConfigParser()
    config.read(_config_file)

    return config.getint('DEFAULT', 'SecondsBetweenChecks')


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
    return last_checked is None or \
        (datetime.now() - last_checked).total_seconds() \
        > seconds_between_checks


def get_pypi_version(name):
    import requests
    try:
        r = requests.get('https://pypi.python.org/pypi/{}/json'.format(name))
    except requests.ConnectionError:
        raise RuntimeError('Failed connection.')
    if not r.ok:
        raise RuntimeError(
            'Response code {} from pypi.python.org.'.format(r.status_code)
            )
    data = r.json()
    return data['info']['version']


def check(name, installed_version, semantic_versioning=True):
    try:
        upstream_version = get_pypi_version(name)
    except RuntimeError:
        return ''
    _log_time(name, datetime.now())

    iv = LooseVersion(installed_version)
    uv = LooseVersion(upstream_version)
    if iv < uv:
        return _get_message(
            name, iv, uv, semantic_versioning=semantic_versioning
            )

    return ''


def _change_in_leftmost_nonzero(a, b):
    leftmost_changed = False
    for k in range(min(len(a), len(b))):
        if a[k] == 0 and b[k] == 0:
            continue
        leftmost_changed = (a[k] != b[k])
        break
    return leftmost_changed


def _get_message(name, iv, uv, semantic_versioning):
    class BashColor(object):
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

    messages = []
    messages.append(
        'Upgrade to   ' +
        BashColor.GREEN +
        '{} {}'.format(name, uv.vstring) +
        BashColor.END +
        '    available! (installed: {})\n'.format(iv.vstring)
        )
    # Check if the leftmost nonzero version number changed. If yes, this means
    # an API change according to Semantic Versioning.
    if semantic_versioning and \
            _change_in_leftmost_nonzero(iv.version, uv.version):
        messages.append((
            BashColor.YELLOW +
            '{}\'s API changes in this upgrade. ' +
            'Changes to your code may be necessary.\n' +
            BashColor.END
            ).format(name))

    three = '3' if sys.version_info >= (3, 0) else ''

    if sys.platform == 'linux' or sys.platform == 'linux2':
        messages.append((
            'To upgrade {} with pip, use\n'
            '\n'
            '   pip{} install -U {}\n'
            '\n'
            'To upgrade _all_ pip-installed packages, use\n'
            '\n'
            '   pipdate{}\n'
            ).format(name, three, name, three))

    messages.append(
        'To disable these checks, '
        'set SecondsBetweenChecks in {} to -1.'.format(_config_file)
        )

    return '\n'.join(messages) + '\n'
