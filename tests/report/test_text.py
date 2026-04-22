"""Tests for text report rendering."""

from se_constitution.report.text import render_validation_report


def test_render_validation_report_for_clean_state() -> None:
    """A clean validation result should render a valid message."""
    report = render_validation_report(errors=[], warnings=[], strict=False)

    assert report == "VALID: constitutional data is internally consistent."


def test_render_validation_report_lists_errors_and_warnings() -> None:
    """Errors and warnings should be rendered in deterministic sections."""
    report = render_validation_report(
        errors=["b error", "a error"],
        warnings=["b warning", "a warning"],
        strict=False,
    )

    assert report == "\n".join(
        [
            "ERRORS:",
            "- a error",
            "- b error",
            "WARNINGS:",
            "- a warning",
            "- b warning",
        ]
    )


def test_render_validation_report_marks_strict_warning_failure() -> None:
    """Strict mode should mark warnings as failure when there are no errors."""
    report = render_validation_report(
        errors=[],
        warnings=["warning"],
        strict=True,
    )

    assert "STRICT MODE: warnings treated as failure." in report
