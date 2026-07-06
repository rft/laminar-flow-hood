"""Work-zone enclosure panels.

Thin side and top walls plus a work-surface deck line the open front section
(Y = 0 .. FILTER_FRONT_Y). They cut cross-drafts that would spoil the
unidirectional flow. The front stays open -- that is where you work.
"""

from __future__ import annotations

from build123d import Compound

from . import config as c
from .geometry import COLORS, box_between

_t = c.PANEL_THICKNESS


def build_walls() -> Compound:
    """Left/right/top walls + deck over the work zone; front left open."""
    y0, y1 = 0.0, c.FILTER_FRONT_Y
    x0, x1 = c.OPENING_X0, c.OPENING_X1
    z0, z1 = c.OPENING_Z0, c.OPENING_Z1

    walls = [
        box_between((x0, y0, z0), (x0 + _t, y1, z1), color=COLORS["wall"], label="wall_left"),
        box_between((x1 - _t, y0, z0), (x1, y1, z1), color=COLORS["wall"], label="wall_right"),
        box_between((x0, y0, z1 - _t), (x1, y1, z1), color=COLORS["wall"], label="wall_top"),
        box_between(
            (x0, y0, z0), (x1, y1, z0 + c.DECK_THICKNESS),
            color=COLORS["deck"], label="deck",
        ),
    ]

    enclosure = Compound(children=walls)
    enclosure.label = "walls"
    return enclosure
