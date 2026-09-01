from parserhub.core.version import get_app_version


def test_get_app_version() -> None:
    app_version = get_app_version()

    assert app_version
    assert isinstance(app_version, str)
