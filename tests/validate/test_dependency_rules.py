"""Tests for dependency rules validation."""

from se_constitution.validate.dependency_rules import validate_dependency_rules
from tests.helpers import get_dependency_rules


def test_validate_dependency_rules_accepts_valid_data() -> None:
    """A valid dependency rules file should produce no errors."""
    data = get_dependency_rules()
    errors = validate_dependency_rules(data)
    assert errors == []
