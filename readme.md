# Laminar Flow Hood

A parametric CAD model (build123d) of a horizontal-flow clean bench built from
aluminium V-slot extrusion, plus the airflow sizing to make it actually work.

See [`docs/laminar_flow.md`](docs/laminar_flow.md) for the design math.

## Run it

```sh
uv run python -m hood     # build the whole hood, print the spec sheet, show it
```

`uv run python frame.py` still works (thin back-compat shim).

## Layout

Everything is modular under `hood/` — one part per module, one shared config:

| Module        | What it is                                             |
|---------------|--------------------------------------------------------|
| `config.py`   | every dimension + design target (the one place to edit)|
| `geometry.py` | shared helpers (`rail`, `box_between`) + colour palette |
| `airflow.py`  | `Q = v·A` sizing, opening area, Reynolds number         |
| `frame.py`    | the extrusion box (`build_frame`)                       |
| `filter.py`   | HEPA panel (`build_filter`)                             |
| `plenum.py`   | sealed pressurised plenum (`build_plenum`)              |
| `blower.py`   | centrifugal blower placeholder (`build_blower`)         |
| `prefilter.py`| coarse intake pre-filter pad (`build_prefilter`)        |
| `panels.py`   | work-zone walls + deck (`build_walls`)                  |
| `assembly.py` | `build_hood()` composes the parts; `report()` prints specs |

Compose the parts yourself:

```python
from hood import build_hood, report
print(report())
hood = build_hood(include={"blower": False})   # omit any part
```

## Bill of materials (frame)

| Qty | Profile | Length | Role                       |
|-----|---------|--------|----------------------------|
| 4   | 2040    | 550 mm | width rails (filter face)  |
| 4   | 2040    | 460 mm | vertical posts             |
| 4   | 2020    | 405 mm | depth rails (airflow path) |

Outer envelope **550 × 405 × 460 mm**, filter opening **470 × 380 mm**,
~**170 CFM** blower at 0.45 m/s face velocity.

## Features / TODO

- LED lights
- Internal power strip
- USB ports
- Linear rails for walls
