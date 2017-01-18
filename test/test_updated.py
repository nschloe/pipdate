import updated


def test_updated():
    updated.get_pypi_version('matplotlib')
    updated.check_and_notify('matplotlib', '0.0.0')
    return
