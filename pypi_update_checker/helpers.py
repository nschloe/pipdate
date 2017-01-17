# -*- coding: utf-8 -*-
#

from packaging import version
import requests


def check(name, installed_version):
    r = requests.get('https://pypi.python.org/pypi/%s/json' % name)
    if r.ok:
        data = r.json()
        upstream_version = data['info']['version']
        if version.parse(installed_version) < version.parse(upstream_version):
            print(
                '\nUpgrade to   %s %s   available! (installed: %s)\n'
                % (name, upstream_version, installed_version)
                )
    return
