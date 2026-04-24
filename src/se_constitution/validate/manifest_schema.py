"""validate/manifest_schema.py - Validation for manifest schema data."""

from se_constitution.types.manifest_schema import ManifestSchemaData


def validate_manifest_schema(data: ManifestSchemaData) -> list[str]:
    """Validate manifest schema structure."""
    errors: list[str] = []

    if "meta" not in data:
        errors.append("manifest-schema.toml: missing [meta] section.")

    if "section" not in data:
        errors.append("manifest-schema.toml: missing [section] section.")
    elif not data["section"]:
        errors.append("manifest-schema.toml: [section] must not be empty.")

    if "field" not in data:
        errors.append("manifest-schema.toml: missing [field] section.")
    elif not data["field"]:
        errors.append("manifest-schema.toml: [field] must not be empty.")

    if "class" not in data:
        errors.append("manifest-schema.toml: missing [class] section.")
    elif not data["class"]:
        errors.append("manifest-schema.toml: [class] must not be empty.")

    return errors
