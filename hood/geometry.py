"""Low-level geometry helpers and the shared colour palette.

Everything here is dumb and reusable: an extrusion-rail factory, an
axis-aligned box between two corner points, and named colours so the parts
are easy to tell apart in the viewer.
"""

from __future__ import annotations

from build123d import Box, Color, Compound, Pos
from bd_vslot.rails import VSlot2020Rail

# Point type: (x, y, z) in mm.
Point = tuple[float, float, float]


# --- Colours (rgba; alpha < 1 is translucent) ----------------------------
COLORS = {
    "aluminum": Color(0.72, 0.74, 0.78),
    "filter": Color(0.95, 0.95, 0.86),
    "prefilter": Color(0.55, 0.70, 0.45),
    "plenum": Color(0.45, 0.55, 0.68, 0.35),
    "blower": Color(0.24, 0.24, 0.28),
    "wall": Color(0.55, 0.78, 0.95, 0.22),
    "deck": Color(0.30, 0.30, 0.34),
}


def rail(length: float, num_x_rails: int = 1, num_y_rails: int = 1) -> VSlot2020Rail:
    """A V-Slot extrusion of `length`, extruded along +Z.

    `num_x_rails=2` -> 2040, `=3` -> 2060, etc. Combine with `num_y_rails`
    for square gangs (e.g. 2x2 -> 4040).
    """
    return VSlot2020Rail(length, num_x_rails=num_x_rails, num_y_rails=num_y_rails)


def box_between(p0: Point, p1: Point, color: Color | None = None, label: str = "") -> Box:
    """An axis-aligned box spanning the two opposite corner points `p0`, `p1`."""
    (x0, y0, z0), (x1, y1, z1) = p0, p1
    part = Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(
        abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)
    )
    if color is not None:
        part.color = color
    if label:
        part.label = label
    return part


def colored(part: Compound, key: str) -> Compound:
    """Tag `part` (and its leaves) with a palette colour, then return it."""
    part.color = COLORS[key]
    for leaf in part.leaves:
        leaf.color = COLORS[key]
    return part
