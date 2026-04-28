# Validation Flow

This document defines how validation is executed across
`se-formal-contract` and `se-constitution`.

It describes the exact sequence required to produce, consume, and
validate the Structural Explainability contract.

## Overview

```text
Lean (formal contract)
    ↓ export
JSON contract artifacts
    ↓ consumed by
Python validation (se-constitution)
```

Validation is only correct if this flow is followed.

## Local validation flow

### Step 1. Build and export formal contract

From `se-formal-contract`:

```shell
lake build
lake exe export_contract
```

This produces:

```text
data/contract/
  invariant-registry.json
  regime-registry.json
  relation-registry.json
  proof-registry.json
```

### Step 2. Commit generated artifacts

```shell
git add data/contract
git commit -m "Update contract artifacts"
```

Generated artifacts must always match Lean output.

### Step 3. Update submodule in `se-constitution`

From `se-constitution`:

```shell
git submodule update --remote external/se-formal-contract
git add external/se-formal-contract
git commit -m "Update formal contract submodule"
```

This pins the new contract version.

### Step 4. Run constitutional validation

```shell
uv run python -m se_constitution validate
```

This validates:

- dependency rules
- class registry consistency
- naming patterns
- manifest schema
- repo requirements
- cross-file consistency
- formal contract invariant binding

### Step 5. Run tests

```shell
uv run pytest
```

## CI validation flow

### `se-formal-contract` CI

```text
lake build
lake exe export_contract
git diff --exit-code data/contract
```

Fails if exported artifacts are not committed.

### `se-constitution` CI

```text
checkout (with submodules)
uv run python -m se_constitution validate
uv run pytest
```

Fails if:

- invariant mismatch
- structural inconsistency
- missing class definitions
- dependency violations

## Key invariants

The following must always hold:

```text
Lean definitions == exported JSON == committed artifacts
```

and:

```text
dependency-rule principles ⊆ invariant registry
```

## Determinism requirement

Validation must be reproducible.

This is achieved by:

- committing generated JSON artifacts
- pinning `se-formal-contract` via submodule
- avoiding network-dependent validation

## Failure modes

### Export drift

```text
Lean output ≠ committed JSON
```

Fix:

```shell
lake exe export_contract
git add data/contract
git commit
```

### Submodule drift

```text
se-constitution references outdated contract
```

Fix:

```shell
git submodule update --remote external/se-formal-contract
```

### Invariant mismatch

```text
dependency rules reference unknown invariant
```

Fix:

- update dependency rules OR
- update formal contract and re-export

### Missing submodule

```text
validation fails due to missing contract files
```

Fix:

```shell
git submodule update --init --recursive
```

## Design constraint

Validation is one-directional:

```text
formal contract → constitution → downstream systems
```

No downstream system may alter the contract.
