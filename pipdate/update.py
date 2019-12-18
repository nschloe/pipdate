import subprocess
import sys


def update_all(user):
    cmd = [sys.executable, "-m", "pip", "list", "--outdated"]
    if user:
        cmd += ["--user"]
    out = subprocess.check_output(cmd).decode("utf-8")
    # The first two lines are
    # ```
    # Package               Version     Latest    Type
    # --------------------- ----------- --------- -----
    # ```
    out = out.split("\n")[2:-1]
    out = [tuple(item.split()[:3]) for item in out]

    # move pip itself to the top of the list
    packages = [item[0] for item in out]
    if "pip" in packages:
        out.insert(0, out.pop(packages.index("pip")))

    cmd = [sys.executable, "-m", "pip", "install"]
    if user:
        cmd += ["--user"]
    cmd += ["--upgrade"]

    for name, old_version, new_version in out:
        print("{} {} -> {}...".format(name, old_version, new_version))
        try:
            subprocess.check_output(cmd + [name])
        except subprocess.CalledProcessError:
            pass
