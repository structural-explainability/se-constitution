"""Shared pytest fixtures."""

from se_constitution.types.primitives import TomlData
from tests.fixture.data import make_valid_data


def valid_data() -> TomlData:
    """Return a valid minimal constitutional dataset."""
    return make_valid_data()
