"""The blower placeholder.

A representative centrifugal ("squirrel-cage") blower mounted on the back
wall, blowing into the plenum. It is a stand-in for sizing/clearance only --
size the real unit for the airflow AND static pressure from airflow.py /
docs/laminar_flow.md (an axial/PC fan will stall against the HEPA).
"""

from __future__ import annotations

from build123d import Compound, Cylinder, Pos, Rot

from . import config as c
from .geometry import COLORS, box_between

_half = c.BLOWER_SIZE / 2


def build_blower() -> Compound:
    """Scroll housing behind the plenum plus its intake throat."""
    cx, cz = c.WIDTH / 2, c.HEIGHT / 2
    y_front, y_back = c.PLENUM_BACK_Y, c.BLOWER_BACK_Y

    housing = box_between(
        (cx - _half, y_front, cz - _half),
        (cx + _half, y_back, cz + _half),
        label="blower_housing",
    )

    # Intake throat: a cylinder on the back of the housing, axis along Y.
    inlet = (
        Pos(cx, y_back + c.BLOWER_INLET_LEN / 2, cz)
        * Rot(-90, 0, 0)
        * Cylinder(c.BLOWER_INLET_R, c.BLOWER_INLET_LEN)
    )
    inlet.label = "blower_inlet"

    blower = Compound(children=[housing, inlet])
    blower.label = "blower"
    for leaf in blower.leaves:
        leaf.color = COLORS["blower"]
    return blower
