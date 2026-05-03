"""validate package for se-constitution.

Re-exports run_validate so callers use:
    from se_constitution.validate import run_validate

rather than importing from orchestrate directly.
"""

from se_constitution.validate.orchestrate import run_validate

__all__ = ["run_validate"]
