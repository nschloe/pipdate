import configparser
import json
import os
import re
import sys
from datetime import datetime

import appdirs
import pkg_resources
from packaging import version

_config_dir = appdirs.user_config_dir("pipdate")
if not os.path.exists(_config_dir):
    os.makedirs(_config_dir)
_config_file = os.path.join(_config_dir, "config.ini")

_log_dir = appdirs.user_log_dir("pipdate", "Nico Schlömer")
if not os.path.exists(_log_dir):
    os.makedirs(_log_dir)
_log_file = os.path.join(_log_dir, "times.log")


def _get_seconds_between_checks():
    if not os.path.exists(_config_file):
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
    if not os.path.exists(_log_file):
        return None
    with open(_log_file) as handle:
        d = json.load(handle)
        if name in d:
            last_checked = datetime.strptime(d[name], "%Y-%m-%d %H:%M:%S")
        else:
            return None
    return last_checked


def _log_time(name, time):
    if os.path.exists(_log_file):
        with open(_log_file) as handle:
            d = json.load(handle)
    else:
        d = {}

    d[name] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(_log_file, "w") as handle:
        json.dump(d, handle)
    return


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
    except requests.ConnectTimeout:
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
        return ""
    _log_time(name, datetime.now())

    print(upstream_version)

    if version.parse(installed_version) >= version.parse(upstream_version):
        return ""

    return _get_message(name, installed_version, upstream_version)


# def _change_in_leftmost_nonzero(a, b):
#     leftmost_changed = False
#     for k in range(min(len(a), len(b))):
#         if a[k] == 0 and b[k] == 0:
#             continue
#         leftmost_changed = a[k] != b[k]
#         break
#     return leftmost_changed


def _is_pip_installed(name):
    try:
        installer = pkg_resources.get_distribution(name).get_metadata("INSTALLER")
    except FileNotFoundError:
        return False
    return installer.strip() == "pip"


def _get_message(name, iv, uv):
    # Inspired by npm's message
    #
    #   ╭─────────────────────────────────────╮
    #   │                                     │
    #   │   Update available 5.5.1 → 6.1.0    │
    #   │     Run npm i -g npm to update      │
    #   │                                     │
    #   ╰─────────────────────────────────────╯
    #
    class BashStyle:
        END = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        BLACK = "\033[30m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        DARKCYAN = "\033[36m"
        LIGHTGRAY = "\033[37m"
        RED = "\033[91m"
        LIGHTYELLOW = "\033[93m"
        BLUE = "\033[94m"
        PURPLE = "\033[95m"
        CYAN = "\033[96m"
        #
        GRAY241 = "\033[38;5;241m"

    if sys.stdout.encoding is None or sys.stdout.encoding.lower() in ("utf-8", "utf8"):
        right_arrow = "\u2192"
        bc = ("╭", "╮", "╰", "╯", "─", "│")
    else:
        right_arrow = "->"
        bc = ("-", "-", "-", "-", "-", "|")

    pip_exe = "pip"

    message = [
        "Update available {}{}{} {} {}{}{}".format(
            BashStyle.GRAY241,
            ".".join(str(k) for k in iv.version),
            BashStyle.END,
            right_arrow,
            BashStyle.GREEN,
            ".".join(str(k) for k in uv.version),
            BashStyle.END,
        )
    ]

    if _is_pip_installed(name):
        message.append(
            ("Run {}{} install -U {}{} to update").format(
                BashStyle.DARKCYAN, pip_exe, name, BashStyle.END
            )
        )
    else:
        message.append(("for package {}").format(name))

    # wrap in frame
    padding_tb = 1
    padding_lr = 3

    border_color = BashStyle.YELLOW

    # https://stackoverflow.com/a/14693789/353337
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    text_width = max(len(ansi_escape.sub("", line)) for line in message)

    out = [
        border_color
        + bc[0]
        + (text_width + 2 * padding_lr) * bc[4]
        + bc[1]
        + BashStyle.END
    ]
    out += padding_tb * [
        border_color
        + bc[5]
        + (text_width + 2 * padding_lr) * " "
        + bc[5]
        + BashStyle.END
    ]

    for line in message:
        length = len(ansi_escape.sub("", line))
        if length < text_width:
            left = (text_width - length) // 2
            right = text_width - length - left
            line = left * " " + line + right * " "
        out += [
            border_color
            + bc[5]
            + BashStyle.END
            + padding_lr * " "
            + line
            + padding_lr * " "
            + border_color
            + bc[5]
            + BashStyle.END
        ]

    out += padding_tb * [
        border_color
        + bc[5]
        + (text_width + 2 * padding_lr) * " "
        + bc[5]
        + BashStyle.END
    ]
    out += [
        border_color
        + bc[2]
        + (text_width + 2 * padding_lr) * bc[4]
        + bc[3]
        + BashStyle.END
    ]

    return "\n".join(out) + "\n"
