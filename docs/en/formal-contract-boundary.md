# Formal Contract Boundary

This document defines how `se-constitution` depends on and interacts with
`se-formal-contract`.

It establishes the authority chain between formal definitions and
operational validation.

## Purpose

`se-formal-contract` defines the **formal, Lean-verified contract** for
Structural Explainability.

`se-constitution` defines the **operational rules and validation logic**
that enforce that contract across repositories.

The boundary ensures:

- a single source of truth for invariants
- no duplication of formal definitions
- deterministic validation behavior

## Authority model

```text
se-formal-contract

  Lean (formal contract)
      ↓ export
  JSON contract artifacts
      ↓ consumed by

se-constitution
  (Python + TOML validation)
```

- The formal contract is **authoritative**.
- `se-constitution` is **constrained by it**, not independent of it.

## Source of truth

- Lean definitions in `se-formal-contract` are canonical.
- JSON artifacts under:

```text
upstream/se-formal-contract/data/contract/
```

are generated outputs.

- `se-constitution` must treat these as **read-only inputs**.

## What `se-constitution` may do

- read invariant, regime, relation, and proof registries
- validate that referenced identifiers exist upstream
- enforce structural consistency across constitutional artifacts

## What `se-constitution` must not do

- redefine invariant identifiers
- introduce new regimes or relations
- reinterpret formal contract semantics
- modify generated contract artifacts

## Current enforcement

`se-constitution` enforces:

- every dependency-rule principle must exist in the
  formal contract invariant registry
- repository classes must remain consistent across all artifacts
- dependency rules must respect constitutional constraints

## Invariant binding

Dependency rules declare principles:

```toml
[principle]
formal_contract_is_root = true
```

These must correspond to invariant identifiers defined in:

```text
upstream/se-formal-contract/data/contract/invariant-registry.json
```

Validation fails if:

- a principle is not declared upstream
- naming diverges from the formal contract

## Submodule requirement

`se-formal-contract` is included as a Git submodule:

```text
upstream/se-formal-contract/
```

All consumers must initialize it:

```shell
git submodule update --init --recursive
```

## Versioning

`se-constitution` is bound to a **specific commit** of
`se-formal-contract`.

Updating the formal contract requires:

1. updating the submodule
2. rerunning validation
3. confirming no invariant mismatches

## Failure modes

### Contract drift

Occurs when:

- submodule is updated without validation
- invariants change upstream without corresponding updates

Result:

- validation errors
- inconsistent rule enforcement

### Boundary violation

Occurs when:

- invariants are redefined locally
- new identifiers are introduced without formal backing

Result:

- loss of authority chain
- divergence from formal guarantees

## Design constraint

The boundary is strict:

```text
Formal layer defines
Operational layer enforces
```

No bidirectional dependency is permitted.
