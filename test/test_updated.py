import updated


def test_updated():
    updated.get_pypi_version('matplotlib')
    updated.needs_checking('matplotlib')
    updated.check('matplotlib', '0.0.0')
    updated.check('requests', '0.0.0')
    updated.needs_checking('matplotlib')
    return
