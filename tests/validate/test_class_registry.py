"""tests/test_class_registry.py - Tests for class registry validation."""

from se_constitution.types.class_registry import ClassRegistryData
from se_constitution.validate.class_registry import validate_class_registry
from tests.helpers import get_class_registry


def test_validate_class_registry_accepts_valid_data() -> None:
    """A valid class registry should produce no errors."""
    data: ClassRegistryData = get_class_registry()

    errors = validate_class_registry(data)

    assert errors == []
