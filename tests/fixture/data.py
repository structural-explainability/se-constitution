"""Minimal valid fixture data for validation tests."""

from se_constitution.types.dependency import DependencyRulesData
from se_constitution.types.primitives import ArtifactCollection


def make_valid_data() -> ArtifactCollection:
    """Return a valid minimal set of data."""
    class_registry = {
        "meta": {"version": "0.1.0", "status": "draft"},
        "class": {
            "constitution": {"summary": "Constitution repo.", "stable": True},
            "kernel": {"summary": "Kernel repo.", "stable": True},
            "schema": {"summary": "Schema repo.", "stable": True},
            "mapspec": {"summary": "Mapspec repo.", "stable": True},
            "mapping": {"summary": "Mapping repo.", "stable": True},
            "adapter": {"summary": "Adapter repo.", "stable": True},
            "profile": {"summary": "Profile repo.", "stable": True},
            "rules": {"summary": "Rules repo.", "stable": True},
            "pilot": {"summary": "Pilot repo.", "stable": False},
            "docs": {"summary": "Docs repo.", "stable": True},
            "policy": {"summary": "Policy repo.", "stable": True},
            "admin": {"summary": "Admin repo.", "stable": True},
        },
    }

    naming_patterns = {
        "meta": {"version": "0.1.0", "status": "draft"},
        "global": {"required_prefix": "se"},
        "pattern": {
            "constitution": {"class": "constitution", "format": "se-constitution"},
            "kernel": {"class": "kernel", "format": "se-kernel"},
            "schema": {"class": "schema", "format": "se-schema-{focus}"},
            "mapspec": {"class": "mapspec", "format": "se-mapspec"},
            "mapping": {"class": "mapping", "format": "se-mapping-{standard}"},
            "adapter": {"class": "adapter", "format": "se-adapter-{standard}"},
            "profile": {
                "class": "profile",
                "format": "se-profile-{jurisdiction}-{focus}",
            },
            "rules": {
                "class": "rules",
                "format": "se-rules-{jurisdiction}-{focus}",
            },
            "pilot": {"class": "pilot", "format": "se-pilot-{focus}"},
            "docs": {"class": "docs", "format": "se-docs-{focus}"},
            "policy": {"class": "policy", "format": "se-policy"},
            "admin": {"class": "admin", "format": "se-admin"},
        },
    }

    dependency_rules: DependencyRulesData = {
        "meta": {"version": "0.1.0", "status": "draft"},
        "dependency": {
            "constitution": {"allowed": []},
            "kernel": {"allowed": ["constitution"]},
            "schema": {"allowed": ["constitution", "kernel"]},
            "mapspec": {"allowed": ["constitution", "kernel", "schema"]},
            "mapping": {"allowed": ["constitution", "kernel", "schema", "mapspec"]},
            "adapter": {"allowed": ["constitution", "kernel", "schema", "mapping"]},
            "profile": {"allowed": ["constitution", "kernel", "schema"]},
            "rules": {"allowed": ["constitution", "kernel", "schema", "profile"]},
            "pilot": {
                "allowed": [
                    "constitution",
                    "kernel",
                    "schema",
                    "mapspec",
                    "mapping",
                    "adapter",
                    "profile",
                    "rules",
                    "docs",
                ]
            },
            "docs": {
                "allowed": [
                    "constitution",
                    "policy",
                    "kernel",
                    "schema",
                    "mapspec",
                    "mapping",
                    "adapter",
                    "profile",
                    "rules",
                ]
            },
            "policy": {"allowed": ["constitution"]},
            "admin": {
                "allowed": [
                    "constitution",
                    "policy",
                    "kernel",
                    "schema",
                    "mapspec",
                    "mapping",
                    "adapter",
                    "profile",
                    "rules",
                    "docs",
                ]
            },
        },
    }

    manifest_schema = {
        "meta": {"version": "0.1.0", "status": "draft"},
        "section": {
            "repo": {"required": True},
            "layer": {"required": True},
            "depends": {"required": True},
        },
        "field": {
            "repo.name": {"type": "string", "required": True},
            "repo.class": {"type": "string", "required": True},
        },
        "class": {
            "constitution": {"required_repo_name_patterns": ["se-constitution"]},
            "kernel": {"required_repo_name_patterns": ["se-kernel"]},
            "schema": {"required_repo_name_patterns": ["se-schema-{focus}"]},
            "mapspec": {"required_repo_name_patterns": ["se-mapspec"]},
            "mapping": {"required_repo_name_patterns": ["se-mapping-{standard}"]},
            "adapter": {"required_repo_name_patterns": ["se-adapter-{standard}"]},
            "profile": {
                "required_repo_name_patterns": ["se-profile-{jurisdiction}-{focus}"]
            },
            "rules": {
                "required_repo_name_patterns": ["se-rules-{jurisdiction}-{focus}"]
            },
            "pilot": {"required_repo_name_patterns": ["se-pilot-{focus}"]},
            "docs": {"required_repo_name_patterns": ["se-docs-{focus}"]},
            "policy": {"required_repo_name_patterns": ["se-policy"]},
            "admin": {"required_repo_name_patterns": ["se-admin"]},
        },
    }

    repo_requirements = {
        "meta": {"version": "0.1.0", "status": "draft"},
        "repo": {
            "constitution": {"summary": "Architectural law."},
            "kernel": {"summary": "Kernel requirements."},
            "schema": {"summary": "Schema requirements."},
            "mapspec": {"summary": "Mapspec requirements."},
            "mapping": {"summary": "Mapping requirements."},
            "adapter": {"summary": "Adapter requirements."},
            "profile": {"summary": "Profile requirements."},
            "rules": {"summary": "Rules requirements."},
            "pilot": {"summary": "Pilot requirements."},
            "docs": {"summary": "Docs requirements."},
            "policy": {"summary": "Policy requirements."},
            "admin": {"summary": "Admin requirements."},
        },
    }

    return {
        "class_registry": class_registry,
        "naming_patterns": naming_patterns,
        "dependency_rules": dict(dependency_rules),
        "manifest_schema": manifest_schema,
        "repo_requirements": repo_requirements,
    }
