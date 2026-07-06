"""The laminar-flow sizing math.

Pure functions over the numbers in `config.py`. See docs/laminar_flow.md
for the derivations and the honest note on what "laminar" means here.
"""

from __future__ import annotations

from . import config as c

CFM_PER_M3S = 2118.88  # 1 m^3/s in cubic feet per minute


def filter_opening() -> tuple[float, float]:
    """Clear filter opening (mm): (width, height)."""
    return c.OPENING_W, c.OPENING_H


def face_area() -> float:
    """Filter face area (m^2) that air actually flows through."""
    return (c.OPENING_W / 1000.0) * (c.OPENING_H / 1000.0)


def required_airflow(velocity: float = c.FACE_VELOCITY) -> dict[str, float]:
    """Airflow the blower must move for a given face `velocity`: Q = v * A."""
    q_m3s = velocity * face_area()
    return {
        "velocity": velocity,
        "area_m2": face_area(),
        "q_m3s": q_m3s,
        "q_m3h": q_m3s * 3600.0,
        "cfm": q_m3s * CFM_PER_M3S,
    }


def reynolds(velocity: float = c.FACE_VELOCITY) -> float:
    """Reynolds number of the discharged sheet (Re = v * D_h / nu).

    D_h = 4A/P is the hydraulic diameter of the opening. This lands in the
    turbulent range on purpose -- a clean bench makes *unidirectional* flow,
    not low-Reynolds laminar flow. See the docs.
    """
    w, h = c.OPENING_W / 1000.0, c.OPENING_H / 1000.0
    perimeter = 2 * (w + h)
    hydraulic_d = 4 * face_area() / perimeter
    return velocity * hydraulic_d / c.AIR_VISCOSITY
