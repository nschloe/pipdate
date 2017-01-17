# pypi_update_checker

[![Code Health](https://landscape.io/github/nschloe/pypi_update_checker/master/landscape.png)](https://landscape.io/github/nschloe/pypi_update_checker/master)
[![PyPi Version](https://img.shields.io/pypi/v/pypi_update_checker.svg)](https://pypi.python.org/pypi/pypi_update_checker)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/pypi_update_checker.svg?style=social&label=Star&maxAge=2592000)](https://github.com/nschloe/pypi_update_checker)

pypi_update_checker checks if a module is older than a release on PyPi, and
prints a warning if necessary.

Using pypi_update_checker is really easy. Simply run
```python
import pypi_update_checker
pypi_update_checker.check_and_notify('matplotlib', '0.4.5')
```
This will print
```
>
> Upgrade to   matplotlib 2.0.0    available! (installed: 0.4.5)
>
> matplotlib's API changes in this upgrade. Changes to your code may be
> necessary.
>
> To upgrade matplotlib with pip, type
>
>    pip install -U matplotlib
>
> To upgrade all pip-installed packages, type
>
>    pip freeze --local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U
>
> To disable these checks, set SecondsBetweenChecks in
> /home/johndoe/.pypi_update_checker to -1.
>
```

### Installation

#### Python Package Index

pypi_update_checker is [available from the Python Package
Index](https://pypi.python.org/pypi/pypi_update_checker/), so simply type
```
pip install pypi_update_checker
```

#### Manual installation

Download pypi_update_checker from
[the Python Package Index](https://pypi.python.org/pypi/pypi_update_checker/).
Place the pypi_update_checker script in a directory where Python can find it
(e.g., `$PYTHONPATH`).  You can install it system-wide with
```
python setup.py install
```
or place the script `pypi_update_checker.py` into the directory where you
intend to use it.


### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    $ make publish
    ```

### License

pypi_update_checker is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
