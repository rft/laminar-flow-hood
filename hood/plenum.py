"""The sealed plenum: the pressurised box behind the filter.

Five thin panels (back, left, right, top, bottom) enclose the gap between
the blower and the filter back face. The filter is the sixth (front) wall.
A pressurised plenum is what makes the exit velocity uniform across the
whole filter face -- seal every seam in the real build.
"""

from __future__ import annotations

from build123d import Compound

from . import config as c
from .geometry import COLORS, box_between

_t = c.PANEL_THICKNESS


def build_plenum() -> Compound:
    """The five-panel plenum skin spanning FILTER_BACK_Y .. PLENUM_BACK_Y."""
    y0, y1 = c.FILTER_BACK_Y, c.PLENUM_BACK_Y
    x0, x1 = c.OPENING_X0, c.OPENING_X1
    z0, z1 = c.OPENING_Z0, c.OPENING_Z1

    panels = [
        box_between((x0, y1 - _t, z0), (x1, y1, z1), label="plenum_back"),
        box_between((x0, y0, z0), (x0 + _t, y1, z1), label="plenum_left"),
        box_between((x1 - _t, y0, z0), (x1, y1, z1), label="plenum_right"),
        box_between((x0, y0, z0), (x1, y1, z0 + _t), label="plenum_bottom"),
        box_between((x0, y0, z1 - _t), (x1, y1, z1), label="plenum_top"),
    ]

    plenum = Compound(children=panels)
    plenum.label = "plenum"
    for leaf in plenum.leaves:
        leaf.color = COLORS["plenum"]
    return plenum
