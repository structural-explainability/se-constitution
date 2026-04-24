# Schema Invariants

Fields and structures that must remain stable across constitutional changes.

## Purpose

- define which fields are load-bearing for validation
- establish contract boundaries for future schema changes
- prevent silent breakage when artifacts evolve

## Stable Field Definition

A "stable field" is a field whose presence, name, and
semantics are required for validation.
Removing or renaming a stable field is a breaking change.

## Breaking Change

A change is considered breaking if it:

- invalidates previously valid artifacts
- changes required field names or meanings
- breaks cross-file contracts

## Class Registry

`class-registry.toml` is the single source of truth for all class names.
Every other artifact is validated against it.

Stable fields:

- `[class]` - must be present and non-empty
- `[class.{name}]` - each entry must define `summary` or `description`

Contract: adding a class is safe;
renaming or removing a class is a breaking change across all five artifacts
(class, naming, dependency, manifest, repo).

## Naming Patterns

Stable fields:

- `[meta]` - must be present
- `[global]` - must be present
- `[pattern]` - must be present and non-empty
- `[pattern.{name}].format` - required per pattern
- `[pattern.{name}].class` - must match a key in `class-registry.toml`

Contract: `class` and `format` are the minimum viable fields per pattern entry.

## Dependency Rules

Stable fields:

- `[meta]` - must be present
- `[dependency]` - must be present
- `[dependency.{name}]` keys - must match keys in `class-registry.toml`
- `[dependency.{name}].allowed` - required; all values must match keys in `class-registry.toml`

Contract: `allowed` is the only semantically enforced field per dependency entry.
Its values are validated against class-registry at runtime.
Single-file validation checks internal structure only; referential integrity
(whether class names are known) is enforced by cross-file validation.

## Manifest Schema

Stable fields:

- `[meta]` - must be present
- `[section]` - must be present
- `[field]` - must be present
- `[class.{name}]` keys - must match keys in `class-registry.toml`

Contract: `section` and `field` define the required structure for
downstream `SE_MANIFEST.toml` files.
Additional constraints may be introduced without
breaking existing valid artifacts.

## Repository Requirements

Stable fields:

- `[meta]` - must be present
- `[repo]` - must be present
- `[repo.{name}]` keys - must match keys in `class-registry.toml`
- `[repo.{name}].summary` - required per class

Contract: `summary` is the minimum required field per repo requirement entry.

## Cross-File Contracts

All cross-file validation is anchored on `class-registry.toml` as the reference set.

The following references must remain consistent across all five artifacts:

| Source file              | Field                           | Must match                        |
| ------------------------ | ------------------------------- | --------------------------------- |
| `naming-patterns.toml`   | `[pattern.*].class`             | `class-registry.toml` class names |
| `dependency-rules.toml`  | `[dependency.*]` keys           | `class-registry.toml` class names |
| `dependency-rules.toml`  | `[dependency.*].allowed` values | `class-registry.toml` class names |
| `manifest-schema.toml`   | `[class.*]` keys                | `class-registry.toml` class names |
| `repo-requirements.toml` | `[repo.*]` keys                 | `class-registry.toml` class names |

## Tests

`tests/validate/test_examples.py`

- canonical examples enforcing invariant compliance
- valid = zero errors
- invalid = deterministic violations

`tests/validate/test_cross_file.py`

- cross-file consistency checks
