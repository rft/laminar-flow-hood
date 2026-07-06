"""Laminar flow hood, modelled part-by-part in build123d.

Public API::

    from hood import build_hood, report
    from hood.frame import build_frame
    from hood.filter import build_filter
    from hood import airflow, config

Run the whole thing with the viewer::

    uv run python -m hood
"""

from __future__ import annotations

from . import airflow, config
from .assembly import build_hood, report
from .blower import build_blower
from .filter import build_filter
from .frame import build_frame
from .panels import build_walls
from .plenum import build_plenum
from .prefilter import build_prefilter

__all__ = [
    "airflow",
    "config",
    "build_hood",
    "report",
    "build_frame",
    "build_filter",
    "build_plenum",
    "build_blower",
    "build_walls",
    "build_prefilter",
]
