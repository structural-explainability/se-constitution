"""Tests for manifest schema validation."""

from typing import cast

from se_constitution.types.cross_file import ManifestSchemaData
from se_constitution.validate.manifest_schema import validate_manifest_schema
from tests.fixture.data import make_valid_data


def get_manifest_schema() -> ManifestSchemaData:
    """Return a valid typed manifest schema artifact.

    WHY:
    TypedDict has no runtime constructor. Use cast at the boundary.
    """
    return cast(ManifestSchemaData, make_valid_data()["manifest_schema"])


def test_validate_manifest_schema_accepts_valid_data() -> None:
    """A valid manifest schema file should produce no errors."""
    data = get_manifest_schema()
    errors = validate_manifest_schema(data)
    assert errors == []
