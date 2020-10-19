# pipdate

[![PyPi Version](https://img.shields.io/pypi/v/pipdate.svg?style=flat-square)](https://pypi.org/project/pipdate)
[![Anaconda Cloud](https://anaconda.org/conda-forge/pipdate/badges/version.svg?=style=flat-square)](https://anaconda.org/conda-forge/pipdate/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pipdate.svg?style=flat-square)](https://pypi.org/pypi/pipdate/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pipdate.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/pipdate)
[![PyPi downloads](https://img.shields.io/pypi/dm/pipdate.svg?style=flat-square)](https://pypistats.org/packages/pipdate)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/pipdate/ci?style=flat-square)](https://github.com/nschloe/pipdate/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pipdate.svg?style=flat-square)](https://codecov.io/gh/nschloe/pipdate)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)


pipdate is a collection of small pip update helpers. The command
```bash
pipdate
# or python3.8 -m pipdate
```
updates _all_ your pip-installed packages. (Only works on Unix.)

There's a Python interface as well that can be used for update notifications.
This
```python
import pipdate
msg = pipdate.check("matplotlib", "0.4.5")
print(msg)
```
will print
<img src="https://github.com/nschloe/pipdate/blob/assets/pipdate.png?raw=true"   width="40%">
<!--
```
╭──────────────────────────────────────────────╮
│                                              │
│       Update available 0.4.5 → 3.1.3         │
│   Run pip install -U matplotlib to update    │
│                                              │
╰──────────────────────────────────────────────╯
```
-->
This can, for example, be used by package authors to notify users of upgrades of
their own packages.

If you guard the check with
```python
if pipdate.needs_checking("matplotlib"):
    print(pipdate.check("matplotlib", "0.4.5"), end="")
```
then it will be performed at most every _k_ seconds, where _k_ is specified
in the config file `$HOME/.config/pipdate/config.ini`, e.g., once a day
```
[DEFAULT]
secondsbetweenchecks = 86400
```

### Installation

pipdate is [available from the Python Package
Index](https://pypi.org/project/pipdate/), so simply type
```
pip install pipdate
```

### Testing

To run the pipdate unit tests, check out this repository and type
```
pytest
```

### License
This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
