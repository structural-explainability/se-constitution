"""sync.py.

Syncs CITATION.cff and pyproject.toml from SE_MANIFEST.toml version.

SE_MANIFEST.toml [contract].contract_version is the canonical version source
for se-constitution. Called automatically by run_validate before checks.
"""

from datetime import date
from pathlib import Path
import re
from typing import Any

from .load import get_consumed_contract_version, load_manifest


def get_manifest_version(manifest: dict[str, Any]) -> str:
    """Extract version from [contract].contract_version."""
    contract = manifest.get("contract")
    if not contract:
        raise ValueError("SE_MANIFEST.toml missing [contract] section")
    version = contract.get("contract_version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("SE_MANIFEST.toml missing or invalid contract_version")
    return version


def sync_citation(version: str) -> None:
    """Update version and date-released in CITATION.cff."""
    path = Path("CITATION.cff")
    if not path.exists():
        raise FileNotFoundError("CITATION.cff not found")

    text = path.read_text(encoding="utf-8")

    text, count_v = re.subn(
        r"(^version:\s*)[^\n]+",
        rf"\g<1>{version}",
        text,
        flags=re.MULTILINE,
    )
    if count_v != 1:
        raise ValueError(f"CITATION.cff: expected 1 version field, found {count_v}")

    today = date.today().isoformat()
    text, count_d = re.subn(
        r"(^date-released:\s*)[^\n]+",
        rf"\g<1>{today}",
        text,
        flags=re.MULTILINE,
    )
    if count_d != 1:
        raise ValueError(
            f"CITATION.cff: expected 1 date-released field, found {count_d}"
        )

    path.write_text(text, encoding="utf-8")


def sync_pyproject(version: str) -> None:
    """Update fallback-version in pyproject.toml."""
    path = Path("pyproject.toml")
    if not path.exists():
        raise FileNotFoundError("pyproject.toml not found")

    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        r'(fallback-version\s*=\s*")[^"]*(")',
        rf"\g<1>{version}\g<2>",
        text,
    )
    if count == 0:
        raise ValueError(
            "pyproject.toml: could not find fallback-version field to update"
        )
    if count > 1:
        raise ValueError(
            f"pyproject.toml: found {count} fallback-version fields - expected exactly 1"
        )
    path.write_text(updated, encoding="utf-8")


def sync_all() -> None:
    """Sync CITATION.cff and pyproject.toml from SE_MANIFEST.toml version."""
    manifest = load_manifest()
    version = get_consumed_contract_version(manifest)
    sync_citation(version)
    sync_pyproject(version)
    print(f"[sync] CITATION.cff and pyproject.toml updated to {version}")
