"""The extrusion box frame, built from the real bill of materials.

    4x 2040 @ 550 mm -> width rails  (X, filter face)
    4x 2040 @ 460 mm -> corner posts (Z)
    4x 2020 @ 405 mm -> depth rails  (Y, airflow path)

Members are placed outer-face-flush so the assembly bounding box is exactly
WIDTH x DEPTH x HEIGHT.
"""

from __future__ import annotations

from build123d import Compound, Pos, Rot

from . import config as c
from .geometry import COLORS, rail


def _z_post(x: float, y: float, num_x_rails: int = 1) -> Compound:
    return Pos(x, y, 0) * rail(c.HEIGHT, num_x_rails=num_x_rails)


def _x_beam(y: float, z: float, num_x_rails: int = 1) -> Compound:
    # Rail extrudes along +Z, so rotate it onto +X.
    return Pos(0, y, z) * Rot(0, 90, 0) * rail(c.WIDTH, num_x_rails=num_x_rails)


def _y_beam(x: float, z: float, num_x_rails: int = 1) -> Compound:
    return Pos(x, 0, z) * Rot(-90, 0, 0) * rail(c.DEPTH, num_x_rails=num_x_rails)


def build_frame() -> Compound:
    """The 4-post / 8-beam box frame."""
    short_half = c.PROFILE / 2             # 10
    # A ganged 2040 sits 10 mm off its placement line (bd_vslot adds the
    # second 2020 to the +local-X side); these offsets shift it back flush.
    gang = (c.PROFILE_LONG - c.PROFILE) / 2  # 10

    parts: list[Compound] = []

    # Vertical posts: 2040 @ HEIGHT. 40 mm face along X, 20 mm along Y.
    for x in (short_half, c.WIDTH - c.PROFILE_LONG + short_half):  # 10, 520
        for y in (short_half, c.DEPTH - short_half):               # 10, 395
            parts.append(_z_post(x, y, num_x_rails=2))

    # Width rails (front/back, top/bottom edges): 2040 @ WIDTH, along X.
    # Bottom face flush at Z=0, top face flush at Z=HEIGHT (the _x_beam gang
    # offset spans [z-(PROFILE_LONG-gang) .. z+gang]).
    for z in (c.PROFILE_LONG - gang, c.HEIGHT - gang):  # 30, 450
        for y in (short_half, c.DEPTH - short_half):    # 10, 395
            parts.append(_x_beam(y, z, num_x_rails=2))

    # Depth rails (left/right, top/bottom edges): 2020 @ DEPTH, along Y.
    for z in (short_half, c.HEIGHT - short_half):    # 10, 450
        for x in (short_half, c.WIDTH - short_half):  # 10, 540
            parts.append(_y_beam(x, z))

    frame = Compound(children=parts)
    frame.label = "frame"
    for leaf in frame.leaves:
        leaf.color = COLORS["aluminum"]
    return frame
