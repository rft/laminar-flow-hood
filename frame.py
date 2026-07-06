"""Laminar flow hood frame, built from V-Slot aluminum extrusion.

Extrusion rails come from `bd_vslot` (2020-based profiles; gang them with
`num_x_rails`/`num_y_rails` to get 2040, 2060, etc.). Joining hardware
(screws, T-nuts) comes from `bd_warehouse`.

Run with the ocp-vscode viewer:
    uv run python frame.py

--- Bill of materials (what you actually have) ---------------------------
    4x  2020  @ 405 mm  -> depth rails    (Y, flow direction)
    4x  2040  @ 460 mm  -> vertical posts (Z, height)
    4x  2040  @ 550 mm  -> width rails    (X, filter-face width)

A cuboid has three sets of four parallel edges, and this inventory is
exactly three sets of four, so the parts map onto a box with no cutting.
The optimal assignment puts the two stiff 2040 sets on the big back face
(which carries the heavy HEPA filter) and the light 2020 set on the short
airflow depth. See docs/laminar_flow.md for the flow/fan sizing.
"""

from __future__ import annotations

from build123d import Compound, Pos, Rot
from bd_vslot.rails import VSlot2020Rail

try:
    from ocp_vscode import show
except ImportError:  # viewer optional
    show = None


# --- Profile cross-sections (mm) -----------------------------------------
PROFILE = 20.0        # 2020 face width (also the short side of a 2040)
PROFILE_LONG = 40.0   # 2040 long side (two 2020s ganged)

# --- Hood outer envelope (mm), measured to the outer faces ---------------
# Each axis is spanned by the four rails of the matching cut length.
WIDTH = 550.0   # left-right  (X)  -- 2040 rails
DEPTH = 405.0   # front-back  (Y)  -- 2020 rails (airflow depth)
HEIGHT = 460.0  # bottom-top  (Z)  -- 2040 posts

# --- Laminar-flow design targets (see docs/laminar_flow.md) --------------
FACE_VELOCITY = 0.45  # m/s, ISO/industry target for a clean bench (0.3-0.5)


def rail(length: float, num_x_rails: int = 1, num_y_rails: int = 1) -> VSlot2020Rail:
    """A V-Slot rail of `length`, extruded along +Z.

    `num_x_rails=2` -> 2040, `=3` -> 2060, etc. Combine with `num_y_rails`
    for square gangs (e.g. 2x2 -> 4040).
    """
    return VSlot2020Rail(length, num_x_rails=num_x_rails, num_y_rails=num_y_rails)


def _z_post(x: float, y: float, length: float, num_x_rails: int = 1) -> Compound:
    """Vertical post at (x, y), spanning 0..length in Z."""
    return Pos(x, y, 0) * rail(length, num_x_rails=num_x_rails)


def _x_beam(x: float, y: float, z: float, length: float, num_x_rails: int = 1) -> Compound:
    """Horizontal beam along +X, starting at (x, y, z)."""
    # Rail extrudes along +Z, so rotate it onto +X.
    return Pos(x, y, z) * Rot(0, 90, 0) * rail(length, num_x_rails=num_x_rails)


def _y_beam(x: float, y: float, z: float, length: float, num_x_rails: int = 1) -> Compound:
    """Horizontal beam along +Y, starting at (x, y, z)."""
    return Pos(x, y, z) * Rot(-90, 0, 0) * rail(length, num_x_rails=num_x_rails)


def build_frame() -> Compound:
    """The 4-post / 8-beam box frame, built from the real inventory.

    Members are placed outer-face-flush, so the assembled bounding box is
    exactly WIDTH x DEPTH x HEIGHT.
    """
    short_half = PROFILE / 2            # 10
    # A ganged 2040 is centered 10 mm off its placement line (bd_vslot adds
    # the second 2020 to the +local-X side). GANG shifts it back to flush.
    gang = (PROFILE_LONG - PROFILE) / 2  # 10

    parts: list[Compound] = []

    # Four vertical corner posts: 2040 @ HEIGHT. The 40 mm face runs along X
    # (in the filter plane), the 20 mm face along Y (into the flow).
    for x in (short_half, WIDTH - PROFILE_LONG + short_half):  # 10, 520
        for y in (short_half, DEPTH - short_half):             # 10, 395
            parts.append(_z_post(x, y, HEIGHT, num_x_rails=2))

    # Top & bottom width rails (front + back edges): 2040 @ WIDTH, along X.
    # Rotated cross-section is 40 (Z, in-plane) x 20 (Y, into the flow).
    for z in (PROFILE_LONG - short_half, HEIGHT - PROFILE_LONG + gang):  # 30, 450
        for y in (short_half, DEPTH - short_half):                       # 10, 395
            parts.append(_x_beam(0, y, z, WIDTH, num_x_rails=2))

    # Top & bottom depth rails (left + right edges): 2020 @ DEPTH, along Y.
    for z in (short_half, HEIGHT - short_half):    # 10, 450
        for x in (short_half, WIDTH - short_half):  # 10, 540
            parts.append(_y_beam(x, 0, z, DEPTH))

    frame = Compound(children=parts)
    frame.label = "hood_frame"
    return frame


def filter_opening() -> tuple[float, float]:
    """Clear inner opening on the back face (mm): (width, height).

    The 2040 perimeter presents its 40 mm face inward on this face, so each
    edge steals PROFILE_LONG from the clear span.
    """
    return WIDTH - 2 * PROFILE_LONG, HEIGHT - 2 * PROFILE_LONG


def required_airflow(velocity: float = FACE_VELOCITY) -> dict[str, float]:
    """Airflow the blower must move to hit `velocity` across the opening.

    Q = v * A. Returns the face area and Q in several units.
    """
    w_mm, h_mm = filter_opening()
    area_m2 = (w_mm / 1000.0) * (h_mm / 1000.0)
    q_m3s = velocity * area_m2
    return {
        "area_m2": area_m2,
        "q_m3s": q_m3s,
        "q_m3h": q_m3s * 3600.0,
        "cfm": q_m3s * 2118.88,
    }


if __name__ == "__main__":
    frame = build_frame()
    bb = frame.bounding_box()
    w_mm, h_mm = filter_opening()
    flow = required_airflow()

    print(f"Frame envelope (mm): {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f}")
    print(f"Members: {len(frame.children)}")
    print(f"Filter opening (mm): {w_mm:.0f} x {h_mm:.0f}  ({flow['area_m2']:.3f} m^2)")
    print(
        f"Airflow @ {FACE_VELOCITY} m/s: "
        f"{flow['q_m3h']:.0f} m^3/h  ({flow['cfm']:.0f} CFM)"
    )
    if show is not None:
        show(frame)
