# -*- coding: utf-8 -*-
#
import pipdate


def test_pipdate():
    pipdate.get_pypi_version("matplotlib")
    pipdate.needs_checking("matplotlib")
    pipdate.check("matplotlib", "0.0.0")
    pipdate.check("requests", "0.0.0")
    pipdate.needs_checking("matplotlib")
    return


if __name__ == "__main__":
    test_pipdate()
