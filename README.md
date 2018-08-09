# pipdate


[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/pipdate/master.svg)](https://circleci.com/gh/nschloe/pipdate/tree/master)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/pipdate.svg)](https://codecov.io/gh/nschloe/pipdate)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPi Version](https://img.shields.io/pypi/v/pipdate.svg)](https://pypi.python.org/pypi/pipdate)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pipdate.svg?logo=github&label=Stars)](https://github.com/nschloe/pipdate)

pipdate is a collection of small pip update helpers. The commands
```
pipdate
pipdate3
```
updates _all_ your pip{3}-installed packages. (Only works on Unix.)

There's a Python interface as well that can be used for update notifications.
This
```python
import pipdate
msg = pipdate.check('matplotlib', '0.4.5')
print(msg)
```
will print
```
╭──────────────────────────────────────────────╮
│                                              │
│        Update available 0.4.5 → 2.2.2        │
│   Run pip3 install -U matplotlib to update   │
│                                              │
╰──────────────────────────────────────────────╯
```

If you guard the check with
```python
if pipdate.needs_checking('matplotlib'):
    print(pipdate.check('matplotlib', '0.4.5'), end='')
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
