# Architecture

This document describes the structure of the Structural Explainability (SE)
foundation layer and how its components interact.

## Overview

Structural Explainability is organized as a layered system:

```text
Formal layer (Lean)
    ↓
Contract artifacts (JSON)
    ↓
Operational validation (Python + TOML)
    ↓
Downstream systems
```

Each layer has a distinct responsibility.

## Core components

### 1. Formal Contract (`se-formal-contract`)

Defines:

- invariants
- regimes
- relations
- proof status

Characteristics:

- implemented in Lean 4
- machine-checked where applicable
- authoritative source of truth

Exports:

```text
data/contract/
  invariant-registry.json
  regime-registry.json
  relation-registry.json
  proof-registry.json
```

### 2. Constitution (`se-constitution`)

Defines:

- repository classes
- dependency rules
- naming patterns
- manifest schema
- repository requirements
- cross-file validation

Consumes:

```text
external/se-formal-contract/data/contract/*.json
```

Responsibilities:

- enforce structural consistency
- validate identifiers against formal contract
- prevent drift across artifacts

## Authority model

```text
se-formal-contract
    defines invariants
        ↓
se-constitution
    enforces usage of invariants
        ↓
downstream repositories
    implement systems using those constraints
```

- authority flows downward only
- no layer may redefine upstream constructs

## Data flow

```text
Lean definitions
    ↓
lake exe export_contract
    ↓
JSON artifacts (committed)
    ↓
submodule (pinned)
    ↓
Python validation
```

Key properties:

- deterministic
- versioned
- reproducible

## Repository structure (foundation layer)

```text
se-formal-contract/
  SEFormalContract/
    Core / Spec / Conformance modules
  data/contract/

se-constitution/
  data/
    class/
    dependency/
    naming/
    manifest/
    repo/
  src/se_constitution/
    validate/
    types/
  external/
    se-formal-contract/   (submodule)
```

## Module design pattern (Lean)

Each domain is split into:

```text
Core        → definitions and theorems
Spec        → identifiers and requirement shapes
Conformance → identifier-to-theorem trace
```

This enables:

- stable identifiers for external systems
- traceability to formal results
- separation of concerns

## Validation model

Validation occurs in `se-constitution`:

1. artifact-level validation
2. cross-file validation
3. formal contract binding

Key rule:

```text
dependency-rule principles ⊆ invariant registry
```

## Determinism

The system enforces determinism by:

- committing generated JSON artifacts
- pinning the formal contract via submodule
- avoiding runtime network dependencies

## Design constraints

- formal definitions must not be duplicated
- identifiers must remain stable once published
- validation must be reproducible
- authority must remain one-directional

## Failure modes

### Contract drift

```text
Lean output ≠ committed JSON
```

### Boundary violation

```text
constitution defines new invariant
```

### Structural inconsistency

```text
missing class / naming / dependency rule
```
