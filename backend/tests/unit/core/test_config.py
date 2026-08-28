from parserhub.core.config import get_settings


def test_get_settings() -> None:
    settings = get_settings()

    assert settings.environment in {"development", "production"}
    assert settings.database_url
    assert settings.secret_key.get_secret_value()
