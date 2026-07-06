"""Compose the individual parts into the full hood and report its specs."""

from __future__ import annotations

from build123d import Compound

from . import airflow, config as c
from .blower import build_blower
from .filter import build_filter
from .frame import build_frame
from .panels import build_walls
from .plenum import build_plenum
from .prefilter import build_prefilter

# Which parts to include, in assembly order. Flip a flag off to omit a part.
PARTS = {
    "frame": build_frame,
    "walls": build_walls,
    "filter": build_filter,
    "plenum": build_plenum,
    "blower": build_blower,
    "prefilter": build_prefilter,
}


def build_hood(include: dict[str, bool] | None = None) -> Compound:
    """The complete laminar flow hood.

    Pass `include={"blower": False, ...}` to leave parts out.
    """
    include = include or {}
    children = [
        build() for name, build in PARTS.items() if include.get(name, True)
    ]
    hood = Compound(children=children)
    hood.label = "laminar_flow_hood"
    return hood


def report() -> str:
    """A human-readable spec sheet for the current config."""
    flow = airflow.required_airflow()
    w, h = airflow.filter_opening()
    lines = [
        "Laminar flow hood -- spec sheet",
        "-" * 40,
        f"Outer envelope : {c.WIDTH:.0f} x {c.DEPTH:.0f} x {c.HEIGHT:.0f} mm (W x D x H)",
        f"Work zone depth: {c.WORK_ZONE_DEPTH:.0f} mm (full interior; stack hangs off back)",
        f"Filter opening : {w:.0f} x {h:.0f} mm  ({flow['area_m2']:.3f} m^2)",
        f"Filter panel   : {c.FILTER_THICKNESS:.0f} mm thick (HEPA H13/H14)",
        f"Plenum gap     : {c.PLENUM_GAP:.0f} mm",
        f"Pre-filter     : {c.PREFILTER_THICKNESS:.0f} mm pad on the intake",
        "",
        f"Target face velocity : {flow['velocity']:.2f} m/s",
        f"Required airflow     : {flow['q_m3h']:.0f} m^3/h  ({flow['cfm']:.0f} CFM)",
        f"Reynolds number      : {airflow.reynolds():.0f}  (turbulent -> unidirectional, not laminar)",
        "",
        "Size the blower for this airflow AT the filter's static pressure",
        "(~0.5-1.0 in. w.g.); see docs/laminar_flow.md.",
    ]
    return "\n".join(lines)
