"""Compatibility shim -- the model now lives in the `hood` package.

Kept so `uv run python frame.py` still works. Prefer:

    uv run python -m hood        # build + show the whole hood
    from hood.frame import build_frame

Each part is its own module under `hood/`:
    config   - every dimension and design target
    airflow  - Q = v*A sizing math (see docs/laminar_flow.md)
    frame    - the extrusion box
    filter / plenum / blower / panels - the parts
    assembly - build_hood() + report()
"""

from __future__ import annotations

from hood.__main__ import main
from hood.frame import build_frame  # noqa: F401  (back-compat re-export)

if __name__ == "__main__":
    main()
