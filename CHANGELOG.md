# Changelog

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

## [Unreleased]

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
- Sample commands:

```shell
# as needed
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0

# new tag / release
git tag v0.1.0 -m "0.1.0"
git push origin v0.1.0
```

[Unreleased]: https://github.com/structural-explainability/se-constitution/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/structural-explainability/se-constitution/releases/tag/v0.1.0
