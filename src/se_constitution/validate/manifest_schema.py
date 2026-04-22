"""Validation for manifest schema data."""

from se_constitution.types.cross_file import ManifestSchemaData


def validate_manifest_schema(data: ManifestSchemaData) -> list[str]:
    """Validate manifest schema structure."""
    errors: list[str] = []

    if "meta" not in data:
        errors.append("manifest-schema.toml: missing [meta] section.")

    if "section" not in data:
        errors.append("manifest-schema.toml: missing [section] section.")

    if "field" not in data:
        errors.append("manifest-schema.toml: missing [field] section.")

    return errors
