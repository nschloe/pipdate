# pipdate

[![Build Status](https://travis-ci.org/nschloe/pipdate.svg?branch=master)](https://travis-ci.org/nschloe/pipdate)
[![codecov](https://codecov.io/gh/nschloe/pipdate/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/pipdate)
[![PyPi Version](https://img.shields.io/pypi/v/pipdate.svg)](https://pypi.python.org/pypi/pipdate)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pipdate.svg?style=social&label=Star&maxAge=2592000)](https://github.com/nschloe/pipdate)

Small pip update helpers.

pipdate checks on PyPi if a given module is outdated. Can be used for upgrade
notifications. Addtionally, it provides the little command-line helper tools
`pipdate`/`pipdate3` for upgrading _all_ pip/pip3-installed packages.

Using pipdate is really easy. Simply run
```python
import pipdate
msg = pipdate.check('matplotlib', '0.4.5')
print(msg)
```
This will print
```
Upgrade to   matplotlib 2.0.0    available! (installed: 0.4.5)

matplotlib's API changes in this upgrade. Changes to your code may be necessary.

To upgrade matplotlib with pip, type

   pip install -U matplotlib

To upgrade _all_ pip-installed packages, use

   pipdate/pipdate3

To disable these checks, set SecondsBetweenChecks in
/home/jdoe/.config/pipdate/config.ini
```

If you guard the check with
```python
if pipdate.needs_checking('matplotlib'):
    print(pipdate.check('matplotlib', '0.4.5'))
```
then it will be performed at most every _k_ seconds, where _k_ is specified
in the config file `$HOME/.config/pipdate/config.ini`, e.g., once a day
```
[DEFAULT]
secondsbetweenchecks = 86400
```

This can, for example, be used by module authors to notify users of upgrades of
their own modules.

### Installation

pipdate is [available from the Python Package
Index](https://pypi.python.org/pypi/pipdate/), so simply type
```
pip install pipdate
```

### Testing

To run the pipdate unit tests, check out this repository and type
```
pytest
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    $ make publish
    ```

### License

pipdate is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
