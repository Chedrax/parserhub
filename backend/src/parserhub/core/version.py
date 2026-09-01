from functools import lru_cache
from importlib.metadata import version as package_version


@lru_cache
def get_app_version() -> str:
    """Return the installed ParserHub package version."""

    return package_version(distribution_name="parserhub")
