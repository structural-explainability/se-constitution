"""Text reporting for validation results."""


def render_validation_report(
    *,
    errors: list[str],
    warnings: list[str],
    strict: bool,
) -> str:
    """Render a deterministic validation report."""
    lines: list[str] = []

    if not errors and not warnings:
        lines.append("VALID: constitutional data is internally consistent.")
        return "\n".join(lines)

    if errors:
        lines.append("ERRORS:")
        for item in sorted(errors):
            lines.append(f"- {item}")

    if warnings:
        lines.append("WARNINGS:")
        for item in sorted(warnings):
            lines.append(f"- {item}")

    if strict and warnings and not errors:
        lines.append("STRICT MODE: warnings treated as failure.")

    return "\n".join(lines)
