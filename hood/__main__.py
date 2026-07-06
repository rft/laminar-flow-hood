"""Entry point: build the hood, print its spec sheet, show it if possible.

    uv run python -m hood
"""

from __future__ import annotations

from .assembly import build_hood, report

try:
    from ocp_vscode import show
except ImportError:  # viewer optional
    show = None


def main() -> None:
    hood = build_hood()
    bb = hood.bounding_box()
    print(report())
    print("-" * 40)
    print(f"Model bounding box (incl. blower): "
          f"{bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"Top-level parts: {[p.label for p in hood.children]}")
    if show is not None:
        show(hood)


if __name__ == "__main__":
    main()
