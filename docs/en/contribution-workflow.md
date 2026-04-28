# Contribution Workflow

This document defines how changes are made across
`se-formal-contract` and `se-constitution`.

## Principles

- Always work from the formal contract outward
- Never duplicate contract definitions
- Keep generated artifacts in sync
- Validate before committing
- Prefer small, complete changes

## Standard workflow

### 1. Make changes in `se-formal-contract` (if needed)

Only if the change affects:

- invariants
- regimes
- relations
- proof status

```shell
cd se-formal-contract
lake build
lake exe export_contract
uv run python -m se_formal_contract validate
uv run pytest
```

### 2. Commit contract changes

```shell
git add -A
git commit -m "Update formal contract"
git push
```

### 3. Update submodule in `se-constitution`

```shell
cd se-constitution
git submodule update --remote external/se-formal-contract
git add external/se-formal-contract
git commit -m "Update formal contract submodule"
```

### 4. Update constitutional artifacts (if needed)

Examples:

- dependency rules
- class registry
- naming patterns
- manifest schema
- repo requirements

### 5. Run validation

```shell
uv run python -m se_constitution validate
uv run pytest
```

### 6. Commit constitutional changes

```shell
git add -A
git commit -m "Update constitutional artifacts"
git push
```

## When to skip steps

- If only documentation changes → skip formal contract + submodule
- If only constitution changes → skip formal contract
- If only tests change → run validation and commit

## Required invariants

The following must always hold:

```text
Lean definitions == exported JSON == committed artifacts
```

and:

```text
dependency-rule principles ⊆ invariant registry
```

## Common tasks

### Add a new invariant

1. Define in Lean (`se-formal-contract`)
2. Export JSON
3. Commit
4. Update submodule
5. Reference in `dependency-rules.toml`
6. Validate

### Modify dependency rules

1. Edit `data/dependency/dependency-rules.toml`
2. Run validation
3. Fix any invariant mismatches
4. Commit

### Fix validation failure

Always read the error message literally.

Typical causes:

- missing class definition
- missing naming pattern
- missing repo requirement
- invariant not declared upstream

## Recovery steps

### Submodule not initialized

```shell
git submodule update --init --recursive
```

### Contract mismatch

```shell
cd se-formal-contract
lake exe export_contract
git add data/contract
git commit
```

## Design constraint

The workflow is directional:

```text
formal-contract → constitution → downstream
```

Never modify downstream layers to compensate for upstream errors.
