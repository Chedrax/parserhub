from fastapi import status
from fastapi.testclient import TestClient

from parserhub.core.config import get_settings
from parserhub.core.version import get_app_version
from parserhub.main import app

client = TestClient(app=app)


def test_version() -> None:
    response = client.get(url="/version")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "version": get_app_version(),
        "environment": get_settings().environment,
    }
