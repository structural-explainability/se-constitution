# Glossary

Canonical definitions for Structural Explainability terms.

## Purpose

- eliminate ambiguity
- support consistent interpretation

## Core Concepts

### Artifact

A structured TOML file that defines part of the Structural Explainability system
(e.g., class registry, naming patterns, dependency rules).

### Constitution

The complete set of artifacts that define the system’s structure, rules, and invariants.

### Class

A named conceptual unit defined in `class-registry.toml` that serves as the reference
set for all other artifacts.

### Contract

A defined expectation about structure or behavior that must hold across artifacts.
Contracts are enforced by validation.

### Cross-File Validation

Validation that ensures consistency between multiple artifacts, especially that
all references resolve to known classes.

### Invariant

A rule that must always hold true for artifacts to be considered valid.
Invariants define the system’s stability boundaries.

### Stable Field

A field whose presence, name, and meaning are required for validation.
Removing or renaming a stable field is a breaking change.

### Breaking Change

A change that invalidates previously valid artifacts, alters required field semantics,
or breaks cross-file contracts.

## Validation Concepts

### Validation

The process of checking artifacts against structural rules and contracts.

### Single-File Validation

Validation of an artifact in isolation, ensuring required fields and structure exist.

### Referential Integrity

The requirement that all referenced values (e.g., class names) exist in the
`class-registry.toml`.

### Error

A violation of an invariant that prevents an artifact set from being valid.

### Warning

A non-fatal condition indicating a potential issue that does not invalidate the system.

## Structural Concepts

### Source of Truth

The authoritative artifact used for validation.
`class-registry.toml` is the system-wide source of truth for class names.

### Pattern

A naming rule defined in `naming-patterns.toml` that associates a format with a class.

### Dependency Rule

A constraint that defines which classes may depend on which other classes.

### Manifest

A downstream artifact (`SE_MANIFEST.toml`) that conforms to the structure defined in
`manifest-schema.toml`.

### Repository Requirement

A definition of what must exist or be documented for a repository per class.

## System Properties

### Lossiness

The degree to which information is lost when transforming or mapping between artifacts
or representations.

- **Lossless**: No information is lost; the original structure can be fully reconstructed.
- **Lossy**: Some information is discarded or cannot be recovered.

In Structural Explainability:

- Cross-file mappings are intended to be **lossless with respect to class identity**
- Transformations (e.g., manifest generation) may be **lossy with respect to structure or context**

### Determinism

The property that validation produces the same results given the same inputs.

### Consistency

The property that all artifacts agree on shared references (e.g., class names).

### Completeness

The degree to which all required structures and references are present.

## Evolution Concepts

### Backward Compatibility

The ability for new versions of the constitution to accept previously valid artifacts.

### Forward Compatibility

The ability for older systems to tolerate newer artifact structures without failure.

### Contract Boundary

The limit beyond which changes are considered breaking.

### Extension

Adding new elements (e.g., classes, patterns) without violating existing contracts.

## Testing Concepts

### Canonical Valid Set

A minimal artifact set that satisfies all invariants and produces zero validation errors.

### Canonical Invalid Set

An artifact set containing deliberate violations used to verify validator behavior.

### Deterministic Violation

A known, reproducible validation failure used for testing correctness.
