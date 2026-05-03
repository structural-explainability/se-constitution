"""load.py - Loading and parsing for the SE constitution.

Provides low-level I/O primitives used by sync.py and validate.py.
No validation logic lives here - only reading and extracting.

Owns:
  - load_toml()                     - read any TOML file
  - load_manifest()                 - read SE_MANIFEST.toml
  - get_consumed_contract_version() - extract contract.contract_version
  - get_git_tag()                   - read current exact git tag

Does not own:
  - validation logic
  - sync logic
  - file writing
"""

from pathlib import Path
import shutil
import subprocess
import tomllib
from typing import Any, cast


def load_toml(path: Path) -> dict[str, Any]:
    """Load and return TOML data from the specified path."""
    return tomllib.loads(path.read_text(encoding="utf-8"))


def require_keys(obj: dict[str, Any], keys: list[str], name: str) -> None:
    """Require that the given object has the specified keys."""
    missing: list[str] = [k for k in keys if k not in obj]
    if missing:
        raise ValueError(f"{name} missing keys: {missing}")


def get_git_tag() -> str:
    """Return the current git tag (exact match required)."""
    git = shutil.which("git")
    if git is None:
        raise RuntimeError("git executable not found on PATH")

    try:
        return (
            subprocess.check_output(  # noqa: S603
                [git, "describe", "--tags", "--exact-match"],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Repository is not on a tagged commit") from exc


def load_manifest() -> dict[str, Any]:
    """Load SE_MANIFEST.toml."""
    path = Path("SE_MANIFEST.toml")
    if not path.exists():
        raise FileNotFoundError("SE_MANIFEST.toml not found")
    return load_toml(path)


def get_consumed_contract_version(manifest: dict[str, Any]) -> str:
    """Extract and validate contract.contract_version from manifest."""
    contract = manifest.get("contract")
    if not isinstance(contract, dict):
        raise ValueError("SE_MANIFEST.toml missing or invalid [contract] section")
    typed: dict[str, object] = cast(dict[str, object], contract)
    version = typed.get("contract_version")
    if not isinstance(version, str):
        raise ValueError(
            "SE_MANIFEST.toml missing or invalid contract.contract_version"
        )
    return version
