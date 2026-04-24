# Examples

Concrete instances of Structural Explainability constitutional artifacts.

## Purpose

- illustrate valid and invalid artifact structures
- support validation testing and adoption

## Valid Set

A minimal two-class ecosystem (`constitution` + `kernel`).
All required fields are present and all cross-file references are consistent.

- `data/examples/valid/class/class-registry.toml`
- `data/examples/valid/naming/naming-patterns.toml`
- `data/examples/valid/dependency/dependency-rules.toml`
- `data/examples/valid/manifest/manifest-schema.toml`
- `data/examples/valid/repo/repo-requirements.toml`

## Invalid Set

The same two-class ecosystem with three deliberate violations.

| #   | File                    | Violation                                              |
| --- | ----------------------- | ------------------------------------------------------ |
| 1   | `class-registry.toml`   | `[class.kernel]` missing required `summary`            |
| 2   | `dependency-rules.toml` | `kernel` allows unknown class `phantom`                |
| 3   | `naming-patterns.toml`  | `[pattern.phantom]` references unknown class `phantom` |

- `data/examples/invalid/class/class-registry.toml`
- `data/examples/invalid/naming/naming-patterns.toml`
- `data/examples/invalid/dependency/dependency-rules.toml`

## Tests

- `tests/validate/test_examples.py`
