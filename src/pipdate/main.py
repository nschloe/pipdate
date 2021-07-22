import configparser
import json
from datetime import datetime
from pathlib import Path

import appdirs
import pkg_resources
from packaging import version
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

_config_dir = Path(appdirs.user_config_dir("pipdate"))
if not _config_dir.exists():
    _config_dir.mkdir(parents=True)
_config_file = _config_dir / "config.ini"

_log_dir = Path(appdirs.user_log_dir("pipdate", "Nico Schlömer"))
if not _log_dir.exists():
    _log_dir.mkdir(parents=True)
_log_file = _log_dir / "times.log"


def _get_seconds_between_checks():
    if not _config_file.exists():
        # add default config
        parser = configparser.ConfigParser()
        parser.set("DEFAULT", "SecondsBetweenChecks", str(24 * 60 * 60))
        with open(_config_file, "w") as handle:
            parser.write(handle)

    # read config
    config = configparser.ConfigParser()
    config.read(_config_file)

    return config.getint("DEFAULT", "SecondsBetweenChecks")


def _get_last_check_time(name):
    if not _log_file.exists():
        return None
    with open(_log_file) as handle:
        d = json.load(handle)
        if name in d:
            last_checked = datetime.strptime(d[name], "%Y-%m-%d %H:%M:%S")
        else:
            return None
    return last_checked


def _log_time(name, time):
    if _log_file.exists():
        with open(_log_file) as handle:
            d = json.load(handle)
    else:
        d = {}

    d[name] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(_log_file, "w") as handle:
        json.dump(d, handle)


def needs_checking(name):
    seconds_between_checks = _get_seconds_between_checks()

    if seconds_between_checks < 0:
        return False

    # get the last time we checked and compare with seconds_between_checks
    last_checked = _get_last_check_time(name)
    return (
        last_checked is None
        or (datetime.now() - last_checked).total_seconds() > seconds_between_checks
    )


def get_pypi_version(name):
    import requests

    try:
        r = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=1.0)
    except requests.Timeout:
        raise RuntimeError("GET requests time out.")
    except requests.ConnectionError:
        raise RuntimeError("Failed connection.")
    if not r.ok:
        raise RuntimeError(f"Response code {r.status_code} from pypi.org.")
    data = r.json()
    return data["info"]["version"]


def check(name, installed_version):
    try:
        upstream_version = get_pypi_version(name)
    except RuntimeError:
        return
    _log_time(name, datetime.now())

    if version.parse(installed_version) >= version.parse(upstream_version):
        return

    return _print_message(name, installed_version, upstream_version)


def _is_pip_installed(name):
    try:
        installer = pkg_resources.get_distribution(name).get_metadata("INSTALLER")
    except FileNotFoundError:
        return False
    return installer.strip() == "pip"


def _print_message(name, iv, uv):
    # Inspired by npm's message
    #
    #   ╭─────────────────────────────────────╮
    #   │                                     │
    #   │   Update available 5.5.1 → 6.1.0    │
    #   │     Run npm i -g npm to update      │
    #   │                                     │
    #   ╰─────────────────────────────────────╯
    #
    # f"Update available {BashStyle.GRAY241}{iv}{BashStyle.END} -> [green]{uv}"
    message = f"Update available [bright_black]{iv}[/] -> [green]{uv}[/]\n"

    if _is_pip_installed(name):
        message += f"Run [dark_cyan]pip install -U {name}[/] to update"
    else:
        message += f"for package {name}"

    # right-justify
    message = Text.from_markup(message, justify="center")

    console = Console()
    console.print(Panel.fit(message, padding=(1, 3), border_style="yellow"))
