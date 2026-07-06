"""The HEPA filter panel.

A solid block standing in for an H13/H14 panel. It fills the clear opening
and forms the front wall of the plenum; its front face is where clean air
enters the work zone. Swap FILTER_THICKNESS / opening in config.py to match
whatever real panel you source.
"""

from __future__ import annotations

from build123d import Compound

from . import config as c
from .geometry import COLORS, box_between


def build_filter() -> Compound:
    """The HEPA panel, filling the opening between the two Y filter planes."""
    return box_between(
        (c.OPENING_X0, c.FILTER_FRONT_Y, c.OPENING_Z0),
        (c.OPENING_X1, c.FILTER_BACK_Y, c.OPENING_Z1),
        color=COLORS["filter"],
        label="hepa_filter",
    )
