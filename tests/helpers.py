"""Test helpers."""

from typing import cast

from se_constitution.types.class_registry import ClassRegistryData
from se_constitution.types.dependency import DependencyRulesData
from tests.fixture.data import make_valid_data


def get_class_registry() -> ClassRegistryData:
    return cast(ClassRegistryData, make_valid_data()["class_registry"])


def get_dependency_rules() -> DependencyRulesData:
    return cast(DependencyRulesData, make_valid_data()["dependency_rules"])
