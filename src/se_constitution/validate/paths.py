"""paths.py - Repository path helpers for se-theory-neutral-substrate.

Owns:
  - repo_root()              - find the repository root
  - reference_dir()          - path to reference/
  - reference_index_path()   - path to reference/index.toml
  - resolve_repo_path()      - resolve repo-relative paths safely

Does not own:
  - file loading
  - validation logic
  - CLI argument parsing
  - synchronization logic

Path helpers keep validation code from scattering hard-coded path literals and
make future path changes local to this module.

Expected local boundaries:
  reference/index.toml declares the repo's public reference artifacts.
  reference/*.toml and reference/*.json are resolved relative to the repo root.

Call chain:
  __main__.py -> cli.main()
              -> orchestrate.run_validate()
              -> validate_reference.validate_reference()
              -> paths.reference_index_path()
"""

from pathlib import Path

_REFERENCE_DIR_NAME = "reference"
_REFERENCE_INDEX_NAME = "index.toml"


def repo_root(start: Path | None = None) -> Path:
    """Find and return the repository root.

    Args:
        start: Optional starting path. Defaults to this file's location.

    Returns:
        Absolute path to the repository root.

    Raises:
        FileNotFoundError: If no repository root marker is found.
    """
    current = (start or Path(__file__)).resolve()

    if current.is_file():
        current = current.parent

    markers = ("pyproject.toml", "SE_MANIFEST.toml", ".git")

    for candidate in (current, *current.parents):
        if any((candidate / marker).exists() for marker in markers):
            return candidate

    raise FileNotFoundError(
        f"Could not find repository root from: {current}. "
        "Expected pyproject.toml, SE_MANIFEST.toml, or .git."
    )


def reference_dir(root: Path | None = None) -> Path:
    """Return the path to reference/."""
    return (root or repo_root()) / _REFERENCE_DIR_NAME


def reference_index_path(root: Path | None = None) -> Path:
    """Return the path to reference/index.toml."""
    return reference_dir(root) / _REFERENCE_INDEX_NAME


def resolve_repo_path(path: str | Path, root: Path | None = None) -> Path:
    """Resolve a repository-relative path safely.

    Args:
        path: Repository-relative path.
        root: Optional repository root. Defaults to repo_root().

    Returns:
        Absolute resolved path.

    Raises:
        ValueError: If path is absolute or resolves outside the repository root.
    """
    repo = (root or repo_root()).resolve()
    relative_path = Path(path)

    if relative_path.is_absolute():
        raise ValueError(
            f"Expected repo-relative path, got absolute path: {relative_path}"
        )

    resolved = (repo / relative_path).resolve()

    try:
        resolved.relative_to(repo)
    except ValueError as e:
        raise ValueError(f"Path escapes repository root: {relative_path}") from e

    return resolved


def reference_artifact_path(path: str | Path, root: Path | None = None) -> Path:
    """Resolve a declared reference artifact path.

    Args:
        path: Repository-relative artifact path declared in reference/index.toml.
        root: Optional repository root. Defaults to repo_root().

    Returns:
        Absolute resolved artifact path.

    Raises:
        ValueError: If the declared path is not under reference/.
    """
    resolved = resolve_repo_path(path, root=root)
    reference = reference_dir(root).resolve()

    try:
        resolved.relative_to(reference)
    except ValueError as e:
        raise ValueError(
            f"Reference artifact path is not under reference/: {path}"
        ) from e

    return resolved
