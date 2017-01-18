# pipdated

[![Build
Status](https://travis-ci.org/nschloe/pipdated.svg?branch=master)](https://travis-ci.org/nschloe/pipdated)
[![Code Health](https://landscape.io/github/nschloe/pipdated/master/landscape.png)](https://landscape.io/github/nschloe/pipdated/master)
[![codecov](https://codecov.io/gh/nschloe/pipdated/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/pipdated)
[![PyPi Version](https://img.shields.io/pypi/v/pipdated.svg)](https://pypi.python.org/pypi/pipdated)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pipdated.svg?style=social&label=Star&maxAge=2592000)](https://github.com/nschloe/pipdated)

pipdated checks on PyPi if a given module is outdated. Can be used for
upgrade notifications.

Using pipdated is really easy. Simply run
```python
import pipdated
msg = pipdated.check('matplotlib', '0.4.5')
print(msg)
```
This will print
```
Upgrade to   matplotlib 2.0.0    available! (installed: 0.4.5)

matplotlib's API changes in this upgrade. Changes to your code may be necessary.

To upgrade matplotlib with pip, type

   pip install -U matplotlib

To upgrade all pip-installed packages, type

   pipdate

To disable these checks, set SecondsBetweenChecks in
/home/jdoe/.config/pipdated/config.ini
```

If you guard the check with
```python
if pipdated.needs_checking('matplotlib'):
    print(pipdated.check('matplotlib', '0.4.5'))
```
then the check will be performed at most every k seconds, where k is specified
in the config file `$HOME/.config/pipdated/config.ini`, e.g., once a day
```
[DEFAULT]
secondsbetweenchecks = 86400
```

This can, for example, be used by module authors to notify users of upgrades of
their own modules.

Additionally, pipdated provides the little command-line helper tool
```
pipdate
```
that updates all pip-installed packages.

### Installation

#### Python Package Index

pipdated is [available from the Python Package
Index](https://pypi.python.org/pypi/pipdated/), so simply type
```
pip install pipdated
```

#### Manual installation

Download pipdated from
[the Python Package Index](https://pypi.python.org/pypi/pipdated/).
Place it in a directory where Python can find it (e.g., `$PYTHONPATH`).  You
can install it system-wide with
```
python setup.py install
```
or place the script `pipdated.py` into the directory where you intend to use
it.

### Testing

To run the pipdated unit tests, check out this repository and type
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

pipdated is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
