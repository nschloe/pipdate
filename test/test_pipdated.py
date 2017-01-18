import pipdated


def test_pipdated():
    pipdated.get_pypi_version('matplotlib')
    pipdated.needs_checking('matplotlib')
    pipdated.check('matplotlib', '0.0.0')
    pipdated.check('requests', '0.0.0')
    pipdated.needs_checking('matplotlib')
    return
