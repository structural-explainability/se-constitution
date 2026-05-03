"""update_lockfile.py.

Reads commit SHA written by sync_upstream.sh, computes a deterministic
SHA-256 hash of the synced contract folder, and writes/updates
upstream/upstream.lock.

Usage: uv run python .github/scripts/update_lockfile.py
Runs from repo root.
"""

from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path

UPSTREAM_DIR = Path("upstream")
LOCK_FILE = Path("upstream/upstream.lock")
COMMIT_TEMP = Path(".github/scripts/_sync_commits.txt")

REPOS = ["se-formal-contract"]


def folder_hash(folder: Path) -> str:
    """Deterministic SHA-256 over all file contents, sorted by path."""
    h = hashlib.sha256()
    for path in sorted(folder.rglob("*")):
        if path.is_file():
            rel = str(path.relative_to(folder))
            h.update(rel.encode())
            h.update(path.read_bytes())
    return f"sha256:{h.hexdigest()}"


def load_commits() -> dict[str, str]:
    """Load repo=commit lines from COMMIT_TEMP into a dict."""
    commits: dict[str, str] = {}
    if COMMIT_TEMP.exists():
        for line in COMMIT_TEMP.read_text().splitlines():
            line = line.strip()
            if "=" in line:
                repo, sha = line.split("=", 1)
                commits[repo.strip()] = sha.strip()
    return commits


def main() -> None:
    """Main function to update the lockfile."""
    commits = load_commits()
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    existing: dict[str, dict[str, str]] = {}
    if LOCK_FILE.exists():
        existing = json.loads(LOCK_FILE.read_text())

    lock: dict[str, dict[str, str]] = {}
    for repo in REPOS:
        folder = UPSTREAM_DIR / repo / "main"
        fhash = folder_hash(folder) if folder.exists() else "sha256:"
        commit = commits.get(repo, existing.get(repo, {}).get("commit", "unknown"))

        lock[repo] = {
            "ref": "main",
            "commit": commit,
            "folder_hash": fhash,
            "synced_at": now,
        }
        print(f"  {repo}: {commit[:12]}  {fhash[:20]}...")

    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(json.dumps(lock, indent=2) + "\n")
    print(f"\nLockfile written: {LOCK_FILE}")

    if COMMIT_TEMP.exists():
        COMMIT_TEMP.unlink()


if __name__ == "__main__":
    main()
