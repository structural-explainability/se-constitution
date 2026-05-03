# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

## [Unreleased]

---

## [0.2.0] - 2026-04-30

### Added

- `theory` repository class for Lean 4 theorem-development repositories
- Naming pattern `se-theory-{focus}` for theory repos
- Dependency rule: `theory` may depend on `formal_contract`
- `theorems` field in `[exports]` section of manifest schema
- `[references]` section in manifest schema for static hand-maintained files
- `load.py` - manifest loading and version extraction primitives
- `sync.py` - syncs `CITATION.cff` and `pyproject.toml` from `SE_MANIFEST.toml` version
- `validate/orchestrate.py` - validation orchestration with auto-sync before checks
- `--require-tag` flag on `validate` command
- `--strict` flag treats warnings as errors

### Changed

- `validate/__init__.py` re-exports `run_validate` as stable public surface
- `cli.py` dispatches to `validate` and `sync` subcommands
- Release procedure updated: `meta.version` in `SE_MANIFEST.toml` is canonical version source

### Fixed

- `app.py` reduced to thin shim

---

## [0.1.1] - 2026-04-27

### Added

New repository classes:

- `regimes` - executable identity and persistence regime repositories
- `govsrc` - traceable governmental source material repositories

Naming pattern support for `govsrc`:

- `se-govsrc-{jurisdiction}`
- `se-govsrc-{jurisdiction}-{focus}`
- Clarified that `{jurisdiction}` may include
  subdivision (e.g., `us-missouri`) and is treated as a single logical token

Dependency rules for new classes:

- `regimes` dependencies aligned with kernel and mapspec layers
- `govsrc` dependencies limited to foundational and specification layers

Repository requirements for new classes:

- `regimes`: executable artifacts with testing and documentation expectations
- `govsrc`: source preservation with provenance and documentation expectations

Documentation structure expectations:

- `docs/regimes` for regime repositories
- `docs/sources` for govsrc repositories

CI execution step:

- Added constitution validation (`se_constitution validate`) as a required CI step

### Changed

Dependency rules registry:

- Standardized format to `[dependency.<class>]` with `allowed` lists
- Alphabetized dependency lists for stability and diff clarity
  Naming patterns:
- Clarified treatment of hyphenated jurisdiction tokens as single logical units

### Fixed

Validation errors for missing dependency rules for `regimes` and `govsrc`

Consistency across:

- class registry
- naming patterns
- dependency rules
- repo requirements

---

## [0.1.0] - 2026-04-22

### Added

- Initial release of constitutional specification and validation framework
- Canonical artifact definitions:
  - class registry
  - dependency rules
  - naming patterns
  - manifest schema
  - repo requirements
- SE_MANIFEST schema (se-manifest-2) and repository declaration model
- Cross-file validation enforcing inter-artifact consistency
- TypedDict-based schema definitions for all artifacts
- Validation modules with test coverage
- Documentation site (folder-based navigation)
- CI: GitHub Actions (lint, type check, tests, docs build)
- Repository hygiene:
  - Ruff (lint and format)
  - pre-commit hooks

---

## Notes on versioning and releases

- We use **SemVer**:
  - **MAJOR** – breaking changes to artifact structure or validation semantics
  - **MINOR** – backward-compatible additions to schema or validation rules
  - **PATCH** – fixes, documentation, tooling
- Versions are driven by git tags. Tag `vX.Y.Z` to release.
- Docs are deployed per version tag and aliased to **latest**.

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. `SE_MANIFEST.toml`

- Update `[contract].contract_version = "X.Y.Z"`

1.2. `CHANGELOG.md`

- Add `## [X.Y.Z] - YYYY-MM-DD`
- Move entries from `[Unreleased]`
- Update comparison links

### Task 2. Sync

```shell
uv run python -m se_constitution sync
```

Reads `SE_MANIFEST.toml` version and updates:

- `CITATION.cff` - `version` and `date-released`

### Task 3. Validate

```shell
uv run python -m se_constitution validate
uvx pre-commit run --all-files
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build
```

### Task 4. Commit, tag, push

```shell
git add .
git commit -m "Release X.Y.Z"
git tag vX.Y.Z -m "X.Y.Z"
git push origin main
git push origin vX.Y.Z
```

- Sample commands:

```shell
# as needed
git tag -d v0.2.0
git push origin :refs/tags/v0.2.0

# new tag / release
git tag v0.2.0 -m "0.2.0"
git push origin v0.2.0
```

## Links

[Unreleased]: https://github.com/structural-explainability/se-constitution/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/structural-explainability/se-constitution/releases/tag/v0.2.0
[0.1.1]: https://github.com/structural-explainability/se-constitution/releases/tag/v0.1.1
[0.1.0]: https://github.com/structural-explainability/se-constitution/releases/tag/v0.1.0
