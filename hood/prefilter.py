"""The intake pre-filter.

A coarse pad (foam / MERV-7-8) over the blower intake. It catches lint and
dust before they reach the HEPA, so the expensive filter lasts far longer.
It is the cheap, replaceable first line of defence -- swap it often.
"""

from __future__ import annotations

from build123d import Compound

from . import config as c
from .geometry import COLORS, box_between

_half = c.PREFILTER_SIZE / 2


def build_prefilter() -> Compound:
    """A square pad just behind the blower intake throat."""
    cx, cz = c.WIDTH / 2, c.HEIGHT / 2
    return box_between(
        (cx - _half, c.PREFILTER_FRONT_Y, cz - _half),
        (cx + _half, c.PREFILTER_BACK_Y, cz + _half),
        color=COLORS["prefilter"],
        label="prefilter",
    )
