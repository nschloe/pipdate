# updated

[![Build
Status](https://travis-ci.org/nschloe/updated.svg?branch=master)](https://travis-ci.org/nschloe/updated)
[![Code Health](https://landscape.io/github/nschloe/updated/master/landscape.png)](https://landscape.io/github/nschloe/updated/master)
[![codecov](https://codecov.io/gh/nschloe/updated/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/updated)
[![PyPi Version](https://img.shields.io/pypi/v/updated.svg)](https://pypi.python.org/pypi/updated)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/updated.svg?style=social&label=Star&maxAge=2592000)](https://github.com/nschloe/updated)

updated checks if a module is older than a release on PyPi, and
prints a warning if necessary.

Using updated is really easy. Simply run
```python
import updated
msg = updated.check('matplotlib', '0.4.5')
print(msg)
```
This will print
```
Upgrade to   matplotlib 2.0.0    available! (installed: 0.4.5)

matplotlib's API changes in this upgrade. Changes to your code may be
necessary.

To upgrade matplotlib with pip, type

   pip install -U matplotlib

To upgrade all pip-installed packages, type

   pip freeze --local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U

To disable these checks, set SecondsBetweenChecks in
/home/jdoe/.config/updated/config.ini
```

If you guard the check with
```python
if updated.needs_checking('matplotlib'):
    print(updated.check('matplotlib', '0.4.5'))
```
then the check will be performed at most every k seconds, where k is specified
in the config file `$HOME/.config/updated/config.ini`
```
[DEFAULT]
secondsbetweenchecks = 86400
```
In this case, the check is only performed at most once every 86400 seconds,
i.e., once a day.

This can, for example, be used by module authors to notify users of upgrades of
their own modules.

### Installation

#### Python Package Index

updated is [available from the Python Package
Index](https://pypi.python.org/pypi/updated/), so simply type
```
pip install updated
```

#### Manual installation

Download updated from
[the Python Package Index](https://pypi.python.org/pypi/updated/).
Place the updated script in a directory where Python can find it
(e.g., `$PYTHONPATH`).  You can install it system-wide with
```
python setup.py install
```
or place the script `updated.py` into the directory where you
intend to use it.

### Testing

To run the updated unit tests, check out this repository and type
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

updated is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
